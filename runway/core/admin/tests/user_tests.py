from ...testing.lib.test_f import RunwayTester
from ...base import DBSession
from ...system.models.user import User, SecurityCheck
import transaction

class RunwaySecurityTester(RunwayTester):
    """
    Used to test the user login security checks
    
    The main difference is a function passed into the get_app function to handle the intermediary step.
    The function should handle the second part of the login process (such as challenge response)
    """
    def get_auth(self, testapp, auth="root"):
        if auth == "":
            return {}
        
        # If it's an integer we need to get their name first
        if type(auth) == int:
            auth = DBSession.query(User.username).filter(User.id == auth).first()
        
        # Now we login
        res = testapp.get('/logout')
        res = testapp.get('/login')
        
        form = res.forms[0]
        
        form.set("username", auth)
        form.set("password", "password")
        res = form.submit('form.submitted')
        
        # If we can't login we want to actually throw an error
        if "Login unsuccessful" in res:
            raise Exception("Unable to login as '%s'" % str(auth))
        
        # We should now get a set of headers, one of which is our new location
        # print(res)
        try:
            res = testapp.get(res.headers['Location'])
        except Exception:
            raise KeyError("Location not found in headers")
        
        
        # This function should now complete the login process
        self.handler_function(self, testapp, res)
        
        # Return the app and cookies for auth
        return testapp


class UserTests(RunwaySecurityTester):
    def test_challenge_response(self):
        with transaction.manager:
            DBSession.execute("""DELETE FROM runway_security_checks WHERE "user" = 1""")
            DBSession.execute("COMMIT")
        
        with transaction.manager:
            sc = SecurityCheck(
                user          = 1,
                check         = "challenge_response",
                data          = "question,answer",
            )
            DBSession.add(sc)
        
        def make_handler(answer):
            def handler_function(self, testapp, response):
                form = response.forms[0]
            
                form.set("challenge_response", answer)
                response = form.submit('form.submitted')
                
                return response
            return handler_function
        
        self.handler_function = make_handler("answer")
        
        app = self.get_app()
        self.make_request(
            app,
            "/",
            "Error logging into the main page",
        )
        
        # Now check it breaks if we answer wrong
        self.handler_function = make_handler("wrong answer")
        
        app = self.get_app()
        self.make_request(
            app,
            "/",
            "Error logging into the main page",
            expect_forward = "/login?redirect=cmVkaXJlY3Q6Oi8=",
        )
    
    
    def test_whitelist_ip(self):
        with transaction.manager:
            DBSession.execute("""DELETE FROM runway_security_checks WHERE "user" = 1""")
            DBSession.execute("COMMIT")
        
        with transaction.manager:
            DBSession.add(SecurityCheck(
                user          = 1,
                check         = "ip_whitelist",
                data          = "127.0.0.1",
            ))
        
        self.handler_function = lambda *args: None
        
        app = self.get_app()
        self.make_request(
            app,
            "/",
            "Error logging into the main page",
        )
        
        # Now ensure we get blocked
        with transaction.manager:
            DBSession.execute("""DELETE FROM runway_security_checks WHERE "user" = 1""")
            DBSession.execute("COMMIT")
        
        with transaction.manager:
            DBSession.add(SecurityCheck(
                user          = 1,
                check         = "ip_whitelist",
                data          = "0.0.0.0",
            ))
        
        self.handler_function = lambda *args: None
        
        try:
            app = self.get_app()
        except Exception as e:
            if e.args[0] == "Location not found in headers":
                pass
            else:
                raise
        else:
            self.fail("IP Whitelist did not stop us logging in from the wrong IP address")
        
    
    
    def test_blacklist_ip(self):
        with transaction.manager:
            DBSession.execute("""DELETE FROM runway_security_checks WHERE "user" = 1""")
            DBSession.execute("COMMIT")
        
        with transaction.manager:
            DBSession.add(SecurityCheck(
                user          = 1,
                check         = "ip_blacklist",
                data          = "0.0.0.0",
            ))
        
        self.handler_function = lambda *args: None
        
        app = self.get_app()
        self.make_request(
            app,
            "/",
            "Error logging into the main page",
        )
        
        # Now ensure we get blocked
        with transaction.manager:
            DBSession.execute("""DELETE FROM runway_security_checks WHERE "user" = 1""")
            DBSession.execute("COMMIT")
        
        with transaction.manager:
            DBSession.add(SecurityCheck(
                user          = 1,
                check         = "ip_blacklist",
                data          = "127.0.0.1",
            ))
        
        self.handler_function = lambda *args: None
        
        try:
            app = self.get_app()
        except Exception as e:
            if e.args[0] == "Location not found in headers":
                pass
            else:
                raise
        else:
            self.fail("IP Blacklist allowed us to log in in from the blocked IP address")
        
    