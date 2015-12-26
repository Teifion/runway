from ...testing.lib.test_f import RunwayTester
from ...base import DBSession
from ...system.models.user import User
import transaction
import re

class AdminTests(RunwayTester):
    def test_general(self):
        app = self.get_app()
        
        self.make_request(
            app,
            "/admin/home",
            "Error trying to view the Admin homepage",
        )
        
        # Test settings window
        res = self.make_request(
            app,
            "/admin/settings",
            "Error trying to view the Admin settings page",
        )
        
        form = res.forms[0]
        form_result = form.submit('form.submitted')
        
        self.check_request_result(
            form_result,
            "There was an error saving site settings in the admin section",
        )
        
        # Site stats
        self.make_request(
            app,
            "/admin/site_stats",
            "Error trying to view the Admin site_stats page",
        )
        
        # Test restart scheduler
        res = self.make_request(
            app,
            "/admin/schedule_restart",
            "Error trying to view the Admin schedule restart page",
        )
        
        form = res.forms[0]
        form.set("date", "2000-01-02")
        form.set("time", "10:12")
        
        form_result = form.submit('form.submitted')
        
        self.check_request_result(
            form_result,
            "There was an error scheduling a restart",
            expect_forward = re.compile(r"/cron/user/edit/[0-9]+"),
        )
    
    def test_user_stuff(self):
        app = self.get_app()
        
        self.make_request(
            app,
            "/admin/user/search_username",
            "Error trying to view admin.user.search_username without data",
        )
        
        self.make_request(
            app,
            "/admin/user/search_username?username=root",
            "Error trying to view admin.user.search_username with a username",
            expect_forward = "/admin/user/edit/1"
        )
        
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
