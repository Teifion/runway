from ...lib import common
import unittest
from datetime import datetime, timedelta, date
from ..lib.test_f import RunwayTesterBase

class CommonTester(RunwayTesterBase):
    def test_as_graceful(self):
        pass
    
    def test_sort_elements(self):
        pass
    
    def test_select_box(self):
        pass
    
    def test_string_to_datetime(self):
        vals = (
            ("2014-01-13", datetime(2014, 1, 13), date(2014, 1, 13)),
            ("2014-01-01", datetime(2014, 1, 1), date(2014, 1, 1)),
            ("2014-12-30", datetime(2014, 12, 30), date(2014, 12, 30)),
            ("2014-03-03", datetime(2014, 3, 3), date(2014, 3, 3)),
            
            # ("3/2/13 10:50:23", datetime(2013, 2, 3, 10, 50, 23), date(2013, 2, 3)),
            # ("3/2/2013 10:50:23", datetime(2013, 2, 3, 10, 50, 23), date(2013, 2, 3)),
        )
        
        for string_date, expected_datetime, expected_date in vals:
            self.assertEqual(expected_datetime, common.string_to_datetime(string_date))
            self.assertEqual(expected_date, common.string_to_date(string_date))
    
    def test_decode(self):
        pass
    
    # def test_dumps(self):
    #     old_print = print
    #     print = lambda x: x
        
    #     output = common.dumps("str")
        
    #     print = old_print
