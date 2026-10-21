"""Generate one immutable specification per JSON row, including pending cells.
This is preparation, not a build. Never generates gameplay or passing evidence.
"""
from dataclasses import make_dataclass, asdict


def generate(sheet):
    specs = []
    for row in sheet['systems']:
        fields = [(key, object) for key in sorted(row)]
        cls = make_dataclass('System_' + row['id'], fields, frozen=True)
        specs.append(asdict(cls(**row)))
    return {'kind': 'unverified-development-specifications', 'systems': specs}
