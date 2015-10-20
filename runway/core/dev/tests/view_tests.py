from ...testing.lib.test_f import RunwayTester
from ...base import DBSession
from ...system.models.user import User
import transaction

class DeveloperTests(RunwayTester):
    def test_general(self):
        app = self.get_app()
        
        self.make_request(
            app,
            "/dev/home",
            "Error trying to view the Developer homepage",
        )
        
        self.make_request(
            app,
            "/testing/preview",
            "Error trying to view the Preview frame homepage",
        )
    
    # def test_user_stuff(self):
    #     app, cookies = self.get_app()
        
    #     self.make_request(
    #         app,
    #         "/list_users",
    #         cookies,
    #         "Error trying to view developer: list users",
    #     )
        
    #     self.make_request(
    #         app,
    #         "/list_users?search_terms=this_is_not_a_user",
    #         cookies,
    #         "Error trying to view developer: list users with search terms",
    #     )
        
    #     self.make_request(
    #         app,
    #         "/list_users?search_terms=jordant",
    #         cookies,
    #         "Error trying to view developer: list users with specific user search",
    #         expect_forward = "/edit_user/1",
    #     )
