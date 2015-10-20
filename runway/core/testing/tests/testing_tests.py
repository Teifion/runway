"""
This is to make sure we're not missing out errors from our templates.

<!--
    The above is a description of an error in a Python program, formatted
for a Web browser because the 'cgitb' module was enabled.  In case you
are not reading this in a Web browser, here is the original traceback:
-->

"""
from ..lib.test_f import RunwayTester
from ...system.lib import errors_f

from ...base import DBSession
from ...system.models.user import UserPermissionGroup
import transaction


class ViewTesterTester(RunwayTester):
    def test_templates(self):
        # We can't use my login because I never get the normal templates (dev)
        app = self.get_app("guest")
        # app = self.get_app()
        
        with transaction.manager:
            DBSession.execute('DELETE FROM {} WHERE "user" = 2;'.format(UserPermissionGroup.__tablename__))
            DBSession.execute("INSERT INTO {} VALUES (2, 'errors');".format(UserPermissionGroup.__tablename__))
            DBSession.execute("COMMIT")
        
        for e_type in ("general", "general_with_message", "graceful"):
            try:
                r = self.make_request(
                    app,
                    "/dev/generate_exception?type=%s" % e_type,
                    "There was an error, but it's okay we're only testing"
                )
            except Exception:
                self.make_request(
                    app,
                    "/dev/exception/hide_all",
                    "Error trying to mark all errors as hidden",
                    expect_forward="/dev/exception/list",
                )
                # if e.args[0] != "There was an error, but it's okay we're only testing":
                #     raise
            else:
                self.fail("No error was raised for the type: {}\n{}".format(e_type,
                """
\033[36mPointer:\033[30;0m The errors are detected by looking for a block of text, it is
probable the block of text was not found in the page source. The block of
text is found in errors_f.traceback_info and is shown below:\n
    {}.""".format(errors_f.traceback_info)))
        
        # Cleanup
        with transaction.manager:
            DBSession.execute('DELETE FROM {} WHERE "user" = 2;'.format(UserPermissionGroup.__tablename__))
            DBSession.execute("COMMIT")
    
    def test_404(self):
        app = self.get_app("guest")
        
        self.assertRaises(AssertionError, self.make_request, *(
            app,
            "/this_is_a_404",
            "The page was a 404"
        ))
    
    def test_forbidden(self):
        app = self.get_app("guest")
        
        self.assertRaises(AssertionError, self.make_request, *(
            app,
            "/edit_user/1",
            "You do not have permission to view this page"
        ))

    def test_forwarder(self):
        app = self.get_app("guest")
        
        self.assertRaises(AssertionError, self.make_request, *(
            app,
            "/edit_user/1",
            "You have been forwarded"
        ))
    
    def test_graceful(self):
        app = self.get_app("guest")
        
        with transaction.manager:
            DBSession.execute('DELETE FROM {} WHERE "user" = 2;'.format(UserPermissionGroup.__tablename__))
            DBSession.execute("INSERT INTO {} VALUES (2, 'errors');".format(UserPermissionGroup.__tablename__))
            DBSession.execute("COMMIT")
        
        self.make_request(
            app,
            "/dev/generate_exception?type=graceful",
            allow_graceful = "This is the message accompanying the general exception."
        )
        
        # Cleanup
        with transaction.manager:
            DBSession.execute('DELETE FROM {} WHERE "user" = 2;'.format(UserPermissionGroup.__tablename__))
            DBSession.execute("COMMIT")
