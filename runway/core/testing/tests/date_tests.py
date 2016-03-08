from ...lib import date_f
import unittest
from datetime import datetime, timedelta, date
from ..lib.test_f import RunwayTesterBase

class CommonTester(RunwayTesterBase):
    def test_empty_inputs(self):
        date_f.get_start_and_end_dates({})
        date_f.get_start_and_end_dates({'start_date':'', 'end_date':''})
        date_f.get_start_and_end_dates({'start_date':' ', 'end_date':' '})
