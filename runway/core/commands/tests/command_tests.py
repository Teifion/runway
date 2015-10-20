from ...testing.lib.test_f import RunwayTester
import unittest
from ...base import DBSession
from ...system.models.user import User
import transaction

from ..lib import funcs

class CommandTests(unittest.TestCase):
    def test_is_int(self):
        vals = (
            ("", False),
            ("A", False),
            (" ", False),
            
            ("1", True),
            ("2", True),
            (2, True),
        )
        
        for value_in, expected in vals:
            result = funcs.is_int(value_in)
            
            self.assertEqual(result, expected, msg="is_int({}) = {} (should be {})".format(
                value_in,
                result,
                expected,
            ))
        
    def test_int_if_int(self):
        vals = (
            ("", ""),
            ("A", "A"),
            (" ", " "),
            
            ("1", 1),
            ("2", 2),
            (2, 2),
        )
        
        for value_in, expected in vals:
            result = funcs.int_if_int(value_in)
            
            self.assertEqual(result, expected, msg="int_if_int({}) = {} (should be {})".format(
                value_in,
                result,
                expected,
            ))
