"""Create a deterministic source-only development archive, never a release."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
from tools.preflight import validate
from tools.generate_contracts import generate

ROOT = Path(__file__).resolve().parents[1]
FILES = ['README.md', 'LICENSE', '.gitignore', 'design/systems.json',
         'research/feasibility.md', 'tools/preflight.py', 'tools/package.py',
         'tools/generate_contracts.py', 'tools/Inspect-LocalGames.ps1',
         'new_eridu/__init__.py', 'new_eridu/contracts.py',
         'tests/test_preflight.py', 'tests/test_development.py']


def package(root, destination):
    sheet = json.loads((root / 'design/systems.json').read_text())
    files = {name: (root / name).read_bytes() for name in FILES}
    files['generated/systems.json'] = json.dumps(generate(sheet), sort_keys=True, indent=2).encode()
    manifest = {'kind': 'development-source-only', 'playable': False,
                'integration_verified': False, 'release_allowed': False,
                'license': 'MIT', 'allow_remix': True,
                'preflight_issues': validate(sheet),
                'sha256': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}
    files['MANIFEST.json'] = json.dumps(manifest, sort_keys=True, indent=2).encode()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return manifest


if __name__ == '__main__':
    if sys.argv[1:] == ['--release']:
        print('Release blocked: installed-game adapters and runtime verification are absent', file=sys.stderr)
        sys.exit(1)
    if sys.argv[1:]:
        print('Usage: python3 -m tools.package [--release]', file=sys.stderr)
        sys.exit(2)
    output = ROOT / 'dist/Fortnite-New-Eridu-development.zip'
    package(ROOT, output)
    print(f'Development source archive only: {output}')
