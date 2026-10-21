"""Validate design sheets; never report unresolved integrations as buildable."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ('id', 'game', 'role', 'integration', 'verification', 'depends_on', 'evidence')


def validate(sheet):
    errors = []
    if not isinstance(sheet, dict):
        return ['sheet: expected object']
    rows = sheet.get('systems', [])
    if not isinstance(rows, list) or not rows:
        return ['systems: missing or empty']
    if any(not isinstance(row, dict) or not isinstance(row.get('id'), str) for row in rows):
        return ['systems: each row requires a string id']
    ids = [row.get('id') for row in rows]
    if len(ids) != len(set(ids)):
        errors.append('systems: duplicate ids')
    for row in rows:
        name = row.get('id', '<missing>')
        for field in FIELDS:
            if field not in row or row[field] is None or row[field] == '':
                errors.append(f'{name}.{field}: unresolved')
        dependencies = row.get('depends_on', [])
        if not isinstance(dependencies, list) or any(not isinstance(x, str) for x in dependencies):
            errors.append(f'{name}.depends_on: expected list of ids')
            dependencies = []
        for dependency in dependencies:
            if dependency not in ids:
                errors.append(f'{name}.depends_on: unknown {dependency}')
        if not isinstance(row.get('evidence'), list) or not row['evidence']:
            errors.append(f'{name}.evidence: runtime verification missing')
        elif any(not isinstance(item, dict) or not all(item.get(key) for key in
                 ('report_path', 'report_sha256', 'host_version', 'companion_version', 'reviewed_by'))
                 for item in row['evidence']):
            errors.append(f'{name}.evidence: incomplete provenance')
        if row.get('integration') is not None and not isinstance(row['integration'], dict):
            errors.append(f'{name}.integration: expected adapter specification')
    by_id = {row.get('id'): row for row in rows}
    active, visited = set(), set()
    def visit(name):
        if name in active:
            errors.append(f'{name}.depends_on: cycle')
            return
        if name in visited:
            return
        active.add(name)
        dependencies = by_id[name].get('depends_on', [])
        if isinstance(dependencies, list):
            for dependency in dependencies:
                if isinstance(dependency, str) and dependency in by_id:
                    visit(dependency)
        active.remove(name)
        visited.add(name)
    for name in by_id:
        visit(name)
    errors.append('runtime: installed-game adapters and independent verification are not implemented')
    for name, game, role in [('host', 'Zenless Zone Zero', 'primary'),
                             ('companion', 'Fortnite', 'companion')]:
        row = by_id.get(name, {})
        if (row.get('game'), row.get('role')) != (game, role):
            errors.append(f'{name}: required game or role changed')
    if sheet.get('license') != 'MIT' or sheet.get('allow_remix') is not True:
        errors.append('license/remix requirements changed')
    if sheet.get('publication_allowed') is not False:
        errors.append('publication is not authorized')
    return errors


def main():
    try:
        sheet = json.loads((ROOT / 'design/systems.json').read_text())
        errors = validate(sheet)
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        print(f'Invalid sheet: {exc}', file=sys.stderr)
        return 2
    print(json.dumps({'build_ready': not errors, 'issues': errors}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
