import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from new_eridu.contracts import require_runtime
from tools.generate_contracts import generate
from tools.package import package, ROOT
from tools.preflight import validate


class DevelopmentTests(unittest.TestCase):
    def setUp(self):
        self.sheet = json.loads((ROOT / 'design/systems.json').read_text())

    def test_generator_preserves_every_cell(self):
        result = generate(self.sheet)
        self.assertEqual(result['systems'], self.sheet['systems'])
        self.assertIsNone(result['systems'][0]['integration'])

    def test_runtime_cannot_fall_back_to_demo(self):
        with self.assertRaisesRegex(RuntimeError, 'no verified'):
            require_runtime()

    def test_cycles_block_build(self):
        self.sheet['systems'][0]['depends_on'] = ['loot']
        self.assertTrue(any('cycle' in error for error in validate(self.sheet)))

    def test_malformed_sheets_are_rejected(self):
        for bad in [None, [], {'systems': {}}, {'systems': [None]}, {'systems': [{'id': []}]}]:
            with self.subTest(bad=bad):
                self.assertTrue(validate(bad))

    def test_claimed_evidence_does_not_unlock_runtime(self):
        for row in self.sheet['systems']:
            row['integration'] = {'adapter': 'not-implemented'}
            row['evidence'] = ['claimed pass']
        errors = validate(self.sheet)
        self.assertTrue(any('incomplete provenance' in error for error in errors))
        self.assertTrue(any('not implemented' in error for error in errors))

    def test_source_archive_is_reproducible_and_checksums_match(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = [Path(directory) / name for name in ('a.zip', 'b.zip')]
            package(ROOT, a)
            package(ROOT, b)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            with zipfile.ZipFile(a) as archive:
                manifest = json.loads(archive.read('MANIFEST.json'))
                self.assertFalse(manifest['playable'])
                self.assertFalse(manifest['release_allowed'])
                self.assertTrue(manifest['preflight_issues'])
                for name, digest in manifest['sha256'].items():
                    self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), digest)
                self.assertFalse(any(name.startswith(('/', '../', '.git/')) for name in archive.namelist()))
                self.assertFalse(any(name.endswith(('.exe', '.dll', '.ucas', '.utoc')) for name in archive.namelist()))

    def test_release_command_fails_without_creating_output(self):
        result = subprocess.run([sys.executable, '-m', 'tools.package', '--release'], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Release blocked', result.stderr)
