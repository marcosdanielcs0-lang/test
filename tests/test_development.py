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


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.routes = json.loads((ROOT / 'design/routes.json').read_text())

    def test_no_selected_route_blocks(self):
        from tools.preflight import validate_routes
        self.assertIn('routes.host: no verified route selected', validate_routes(self.routes))

    def test_visual_route_cannot_host_gameplay_even_if_other_flags_claim_pass(self):
        from tools.preflight import validate_routes
        self.routes['selected']['host'] = 'zzmi'
        row = self.routes['routes'][0]
        row.update(permitted=True, melty_one_click_verified=True, steam_verified=True,
                   runtime_evidence=['claimed'], blockers=[])
        self.assertIn('routes.host.capabilities: insufficient', validate_routes(self.routes))

    def test_one_click_and_permission_are_separate_requirements(self):
        from tools.preflight import validate_routes
        self.routes['selected']['host'] = 'bepinex'
        errors = validate_routes(self.routes)
        self.assertIn('routes.host.permitted: not verified', errors)
        self.assertIn('routes.host.melty_one_click_verified: not verified', errors)
        self.assertIn('routes.host.steam_verified: not verified', errors)

    def test_route_references_resolve(self):
        sheet = json.loads((ROOT / 'design/systems.json').read_text())
        sheet['systems'][0]['candidate_routes'] = ['imaginary']
        self.assertIn('host.candidate_routes: unknown imaginary', validate(sheet, self.routes))

    def test_source_references_resolve(self):
        sources = json.loads((ROOT / 'research/route-sources.json').read_text())
        ids = {row['id'] for row in sources['sources']}
        for route in self.routes['routes']:
            self.assertTrue(set(route['sources']).issubset(ids), route['id'])


class SinglePlayerTests(unittest.TestCase):
    def setUp(self):
        self.systems = json.loads((ROOT / 'design/systems.json').read_text())
        self.missions = json.loads((ROOT / 'design/missions.json').read_text())
        self.acceptance = json.loads((ROOT / 'design/acceptance.json').read_text())

    def test_scope_has_no_cooperation_system_or_references(self):
        self.assertEqual(self.systems['mode'], 'single-player')
        self.assertEqual(self.systems['player_count'], 1)
        self.assertEqual({r['id'] for r in self.systems['systems']},
                         {'host', 'companion', 'missions', 'combat', 'loot'})
        for row in self.systems['systems']:
            self.assertNotIn('cooperation', row['depends_on'])

    def test_regression_to_multiplayer_is_rejected(self):
        from tools.preflight import validate_single_player
        self.systems['mode'] = 'multiplayer'
        self.systems['player_count'] = 2
        self.assertIn('scope: requires single-player with one player',
                      validate_single_player(self.systems, self.missions, self.acceptance))

    def test_mission_pending_hooks_cannot_pass(self):
        from tools.preflight import validate_single_player
        errors = validate_single_player(self.systems, self.missions, self.acceptance)
        self.assertIn('missions.first-solo-pve.host_mission_hook: unresolved', errors)
        self.assertIn('missions.first-solo-pve.fortnite_contribution: unresolved', errors)
        self.assertIn('missions.first-solo-pve.loot_hook: unresolved', errors)

    def test_acceptance_cannot_drop_real_companion(self):
        from tools.preflight import validate_single_player
        self.acceptance['criteria'] = [r for r in self.acceptance['criteria'] if r['id'] != 'real-companion']
        errors = validate_single_player(self.systems, self.missions, self.acceptance)
        self.assertIn('acceptance: required criteria missing, duplicated or unexpected', errors)

    def test_mission_references_cannot_point_to_deleted_cooperation(self):
        from tools.preflight import validate_single_player
        self.missions['missions'][0]['system_refs'].append('cooperation')
        self.assertIn('missions.first-solo-pve.system_refs: required references do not resolve',
                      validate_single_player(self.systems, self.missions, self.acceptance))

    def test_solo_route_does_not_require_multiplayer(self):
        # Synthetic metadata tests the validator only, not gameplay or installation.
        from tools.preflight import validate_routes
        routes = {'selected': {'host': 'h', 'companion': 'c'}, 'routes': [
            {'id': 'h', 'side': 'host', 'capabilities': ['missions', 'combat-pve', 'loot'],
             'permitted': True, 'steam_verified': True, 'melty_one_click_verified': True,
             'runtime_evidence': ['unit-test-only'], 'blockers': []},
            {'id': 'c', 'side': 'companion', 'capabilities': ['real-content-or-events'],
             'permitted': True, 'melty_one_click_verified': True,
             'runtime_evidence': ['unit-test-only'], 'blockers': []}]}
        self.assertEqual(validate_routes(routes), [])
        routes['routes'][0]['capabilities'].remove('combat-pve')
        self.assertIn('routes.host.capabilities: insufficient', validate_routes(routes))

    def test_package_carries_current_solo_design_and_pending_acceptance(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'source.zip'
            manifest = package(ROOT, output)
            self.assertEqual(manifest['mode'], 'single-player')
            self.assertEqual(manifest['player_count'], 1)
            with zipfile.ZipFile(output) as archive:
                for name in ['design/missions.json', 'design/acceptance.json', 'design/routes.json']:
                    self.assertIn(name, archive.namelist())
                acceptance = json.loads(archive.read('design/acceptance.json'))
                self.assertTrue(all(r['status'] == 'pending' for r in acceptance['criteria']))


if __name__ == '__main__':
    unittest.main()
