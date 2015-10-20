from ...testing.lib.test_f import RunwayTester
from ...base import DBSession
from ...system.models.user import User
import transaction

class AdminTests(RunwayTester):
    def test_general(self):
        app = self.get_app()
        
        self.make_request(
            app,
            "/documentation/home",
            "Error trying to view the Documentation homepage",
        )
