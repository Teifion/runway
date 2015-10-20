import unittest
from ..lib import form_validation as fv

class FakeRequest(object):
    def __init__(self, params):
        self.params = params

def make_request(**params):
    return FakeRequest(params)

generic_request = make_request(
    spaces = "   ",
    zeroes = "000",
                               
    good_empty_value = "",
    bad_empty_value = "text",
    
    good_int_value = "10",
    bad_int_value = "text",
    
    good_float_value = "3.14",
    bad_float_value = "text",
    
    has_spaces = "text1 text2",
)

class FunctionTester(unittest.TestCase):
    def test_validation_basics(self):
        results, errors = fv.validate_form(generic_request,
            ("good_empty_value", str, fv.non_empty),
            ("bad_empty_value", str, fv.non_empty),
            # ("bad_empty_value", str, fv.non_empty),
        )
        
        self.assertEqual(results['good_empty_value'], "")
        self.assertEqual(results['bad_empty_value'], "text")
        
        self.assertEqual(errors['good_empty_value'], ["Expected a non-empty value"])
        
