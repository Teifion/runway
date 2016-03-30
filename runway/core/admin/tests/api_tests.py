from ...testing.lib.test_f import RunwayTester
from ...base import DBSession
from ...system.models.user import User
from ...apis.lib import api_f
import json
import transaction

class UserTests(RunwayTester):
    def test_daily_usage_api(self):
        app = self.get_app()
        
        dev_key = api_f.get_key_by_user(1).key
        
        # system.users
        r = self.make_request(
            app,
            "/api/request?request=admin.usage&key={}".format(dev_key),
            "admin.usage API test",
        )
        
        api_result = api_f.test_response(r, " - system.users API test")
        if api_result:
            self.fail(api_result)
        
        # Check it's valid json
        json.loads(r.body.decode('utf-8'))
