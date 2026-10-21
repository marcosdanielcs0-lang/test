import copy
import json
from pathlib import Path
import unittest
from tools.preflight import validate


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.sheet = json.loads((Path(__file__).resolve().parents[1] / 'design/systems.json').read_text())

    def test_current_design_is_blocked(self):
        errors = validate(self.sheet)
        self.assertIn('companion.integration: unresolved', errors)
        self.assertIn('host.evidence: runtime verification missing', errors)

    def test_unknown_reference_is_rejected(self):
        self.sheet['systems'][0]['depends_on'] = ['nonexistent']
        self.assertIn('host.depends_on: unknown nonexistent', validate(self.sheet))

    def test_role_substitution_is_rejected(self):
        self.sheet['systems'][1]['role'] = 'secondary'
        self.assertIn('companion: required game or role changed', validate(self.sheet))

    def test_duplicate_id_is_rejected(self):
        self.sheet['systems'].append(copy.deepcopy(self.sheet['systems'][0]))
        self.assertIn('systems: duplicate ids', validate(self.sheet))

    def test_empty_sheet_is_rejected(self):
        self.assertTrue(validate({'systems': []}))


if __name__ == '__main__':
    unittest.main()
