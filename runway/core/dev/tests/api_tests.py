from ...testing.lib.test_f import RunwayTester
from ...apis.lib import api_f

class DevTests(RunwayTester):
    def test_runway_dev_api(self):
        app = self.get_app()
        
        dev_key = api_f.get_key_by_user(1).key
        
        # system.users
        r = self.make_request(
            app,
            "/api/request?request=dev.exception_count&key={}".format(dev_key),
            "system.users API test",
        )
        
        api_result = api_f.test_response(r, " - dev.exception_count API test")
        if api_result:
            self.fail(api_result)
        
        # Check it's a number
        r = int(r.body)
