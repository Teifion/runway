from ...testing.lib.test_f import RunwayTester
from ...base import DBSession
from ...system.models.user import User
import transaction

password_hash = '$5$rounds=110000$A1vz94RZAKWk6mzf$mqMkuKbzKrNOddYhVnnElAPG0KQImtds6kQX1iSThf6'

class UserTests(RunwayTester):
    def test_homepage(self):
        app = self.get_app()
        
        self.make_request(
            app,
            "/",
            "Error trying to view the Runway homepage",
        )
    
    def test_general(self):
        with transaction.manager:
            DBSession.execute("DELETE FROM {} WHERE id = -6789".format(User.__tablename__))
            DBSession.execute("COMMIT")
        
        with transaction.manager:
            DBSession.add(User(
                id = -6789,
                username = 'password_change_test_account',
                display_name = 'password_change_test_account',
                password = password_hash,
            ))
        
        app = self.get_app('password_change_test_account')
        
        self.make_request(
            app,
            "/",
            "Error trying to view homepage",
        )
        
        page_result = self.make_request(
            app,
            "/user/account",
            "Error trying to view user control panel",
        )
        
        # Invalid new password, too short
        form = page_result.form
        form.set("current_password", "password")
        form.set("new_password1", "123")
        form.set("new_password2", "123")
        form_result = form.submit('form.submitted')
        
        self.check_request_result(
            form_result,
            "There was an error changing the password to an too short a password",
            allow_graceful = "Your password must be at least 8 characters long.",
        )
        
        # Invalid new password, banned password
        form.set("current_password", "password")
        form.set("new_password1", "password")
        form.set("new_password2", "password")
        form_result = form.submit('form.submitted')
        
        self.check_request_result(
            form_result,
            "There was an error changing the password to an invalid password",
            allow_graceful = """You cannot change your password to "password".""",
        )
        
        # Now use a valid password but enter our current one wrong
        form.set("current_password", "password_is_wrong")
        form.set("new_password1", "1234567890")
        form.set("new_password2", "1234567890")
        form_result = form.submit('form.submitted')
        
        self.check_request_result(
            form_result,
            "There was an error changing the password",
        )
        
        password_user = DBSession.query(User).filter(User.id == -6789).first()
        self.assertEqual(password_user.password, password_hash, msg="The password was chaneged even though we entered our current password incorrectly")
        
        # Now use a valid password but the passwords don't match
        # note: this should be blocked by the javascript but it's always best to be sure
        form.set("current_password", "password")
        form.set("new_password1", "1234567890_wrong")
        form.set("new_password2", "1234567890")
        form_result = form.submit('form.submitted')
        
        self.check_request_result(
            form_result,
            "There was an error changing the password",
        )
        
        password_user = DBSession.query(User).filter(User.id == -6789).first()
        self.assertEqual(password_user.password, password_hash, msg="The password was chaneged even though password1 and password2 did not match")
        
        # Now do it correctly
        form.set("current_password", "password")
        form.set("new_password1", "1234567890")
        form.set("new_password2", "1234567890")
        form_result = form.submit('form.submitted')
        
        page_result = self.check_request_result(
            form_result,
            "There was an error changing the password",
        )
        
        password_user = DBSession.query(User).filter(User.id == -6789).first()
        self.assertNotEqual(password_user.password, password_hash, msg="The password was not correctly changed")

