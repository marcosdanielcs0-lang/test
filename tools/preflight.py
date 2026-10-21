"""Validate design sheets; never report unresolved integrations as buildable."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ('id', 'game', 'role', 'integration', 'verification', 'depends_on', 'evidence')


ACCEPTANCE_IDS = {'host-runtime', 'real-companion', 'solo-mission', 'pve-combat',
                  'loot', 'allowed-install', 'real-evidence'}
EXCLUDED = {'multiplayer', 'player-cooperation', 'network-synchronization', 'own-servers'}


def validate_single_player(systems, missions, acceptance):
    errors = []
    if systems.get('mode') != 'single-player' or systems.get('player_count') != 1:
        errors.append('scope: requires single-player with one player')
    ids = {row['id'] for row in systems['systems']}
    if ids != {'host', 'companion', 'missions', 'combat', 'loot'}:
        errors.append('scope: expected host, companion, missions, combat and loot only')
    if not isinstance(acceptance, dict) or not isinstance(acceptance.get('criteria'), list):
        errors.append('acceptance: missing or invalid sheet')
        criteria = []
    else:
        criteria = acceptance['criteria']
        if acceptance.get('mode') != 'single-player' or acceptance.get('player_count') != 1:
            errors.append('acceptance: single-player scope required')
        excluded = acceptance.get('excluded_requirements', [])
        if not isinstance(excluded, list) or any(not isinstance(x, str) for x in excluded) or set(excluded) != EXCLUDED:
            errors.append('acceptance: excluded requirements changed')
    valid_rows = [row for row in criteria if isinstance(row, dict) and isinstance(row.get('id'), str)]
    criterion_ids = {row['id'] for row in valid_rows}
    if len(valid_rows) != len(criteria) or len(criterion_ids) != len(criteria) or criterion_ids != ACCEPTANCE_IDS:
        errors.append('acceptance: required criteria missing, duplicated or unexpected')
    for row in valid_rows:
        if row.get('required') is not True or row.get('status') != 'passed' or not row.get('evidence'):
            errors.append(f"acceptance.{row['id']}: real-game verification pending")
    if not isinstance(missions, dict) or not isinstance(missions.get('missions'), list) or not missions['missions']:
        return errors + ['missions: missing or empty sheet']
    if missions.get('mode') != 'single-player':
        errors.append('missions: single-player scope required')
    seen = set()
    for row in missions['missions']:
        if not isinstance(row, dict) or not isinstance(row.get('id'), str):
            errors.append('missions: each row requires a string id')
            continue
        name = row['id']
        if name in seen:
            errors.append(f'missions.{name}: duplicate id')
        seen.add(name)
        for field in ('host_mission_hook', 'pve_event_hook', 'fortnite_contribution', 'loot_hook', 'reward_definition'):
            if not row.get(field):
                errors.append(f'missions.{name}.{field}: unresolved')
        for field, required in [('system_refs', ids), ('acceptance_refs', ACCEPTANCE_IDS)]:
            refs = row.get(field)
            if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs) or set(refs) != required:
                errors.append(f'missions.{name}.{field}: required references do not resolve')
        if row.get('status') != 'verified' or not row.get('runtime_evidence'):
            errors.append(f'missions.{name}: runtime evidence missing')
    return errors


def validate_routes(sheet):
    if not isinstance(sheet, dict) or not isinstance(sheet.get('routes'), list):
        return ['routes: missing or invalid sheet']
    errors = []
    rows = sheet['routes']
    if any(not isinstance(row, dict) or not isinstance(row.get('id'), str) for row in rows):
        return ['routes: each row requires a string id']
    by_id = {row['id']: row for row in rows}
    if len(by_id) != len(rows):
        errors.append('routes: duplicate ids')
    selected = sheet.get('selected', {})
    if not isinstance(selected, dict):
        return errors + ['routes.selected: expected object']
    for side, required in [('host', {'missions', 'combat-pve', 'loot'}),
                           ('companion', {'real-content-or-events'})]:
        name = selected.get(side)
        if not isinstance(name, str) or name not in by_id:
            errors.append(f'routes.{side}: no verified route selected')
            continue
        row = by_id[name]
        if row.get('side') != side:
            errors.append(f'routes.{side}: wrong role')
        for field in ('permitted', 'melty_one_click_verified'):
            if row.get(field) is not True:
                errors.append(f'routes.{side}.{field}: not verified')
        if side == 'host' and row.get('steam_verified') is not True:
            errors.append('routes.host.steam_verified: not verified')
        capabilities = row.get('capabilities', [])
        if not isinstance(capabilities, list) or any(not isinstance(x, str) for x in capabilities):
            capabilities = []
        if not required.issubset(capabilities):
            errors.append(f'routes.{side}.capabilities: insufficient')
        if not isinstance(row.get('runtime_evidence'), list) or not row['runtime_evidence']:
            errors.append(f'routes.{side}: runtime evidence missing')
        if row.get('blockers') != []:
            errors.append(f'routes.{side}: unresolved blockers')
    return errors


def validate(sheet, routes=None, missions=None, acceptance=None):
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
    errors.extend(validate_routes(routes))
    errors.extend(validate_single_player(sheet, missions, acceptance))
    if isinstance(routes, dict) and isinstance(routes.get('routes'), list):
        route_ids = {row['id'] for row in routes['routes']
                     if isinstance(row, dict) and isinstance(row.get('id'), str)}
        for row in rows:
            candidates = row.get('candidate_routes', [])
            if not isinstance(candidates, list) or any(not isinstance(x, str) for x in candidates):
                errors.append(f"{row['id']}.candidate_routes: invalid list")
            else:
                for name in candidates:
                    if name not in route_ids:
                        errors.append(f"{row['id']}.candidate_routes: unknown {name}")
    return errors


def main():
    try:
        sheet = json.loads((ROOT / 'design/systems.json').read_text())
        routes = json.loads((ROOT / 'design/routes.json').read_text())
        missions = json.loads((ROOT / 'design/missions.json').read_text())
        acceptance = json.loads((ROOT / 'design/acceptance.json').read_text())
        errors = validate(sheet, routes, missions, acceptance)
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        print(f'Invalid sheet: {exc}', file=sys.stderr)
        return 2
    print(json.dumps({'build_ready': not errors, 'issues': errors}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
