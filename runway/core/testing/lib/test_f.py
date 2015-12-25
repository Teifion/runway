from datetime import datetime, timedelta
import itertools
import sys
import unittest
import random
import http.cookiejar

import transaction
from pyramid import testing, renderers
from webtest import TestApp

from ...triggers.lib import triggers_f

import re

from ...base import (
    Base,
    DBSession,
)
from ...system.models.user import User

from ...system.lib import errors_f, site_settings_f

from ...main import main, routes, plugin_routes

class AlwaysTrueDict(object):
    def __getitem__(self, key): return 'True'
    def get(self, key, default=None): return 'True'

engine_str = "postgresql+pypostgresql://postgres:qwfpgj@localhost:5432/venustate_testing"

def DummyRequest(user_level = "developer"):
    r = testing.DummyRequest()
    
    if user_level == "developer":
        r.user = User()
    else:
        raise Exception("No handler for user_level '%s'" % user_level)
    
    return r

find_error = re.compile(r"Traceback \(most recent call last\):(.+?)-->", re.DOTALL)
find_graceful = re.compile(r"<!-- start_graceful_message -->(.+?)<!-- end_graceful_message -->", re.DOTALL)
find_exception = re.compile(r"<!-- start of traceback -->(.+?)<!-- end of traceback -->", re.DOTALL)
def _initTestingDB():
    from sqlalchemy import create_engine
    
    engine = create_engine(engine_str)
    # Base.metadata.create_all(engine)
    # DBSession.configure(bind=engine, autocommit=True)
    DBSession.configure(bind=engine)
    
    return DBSession

class RunwayTesterBase(unittest.TestCase):
    _multiprocess_can_split_ = True    

class RunwayTester(RunwayTesterBase):
    plugin_name = None
    
    def setUp(self):
        self.session = _initTestingDB()
        self.config = plugin_routes(routes(testing.setUp()), route_settings=AlwaysTrueDict())
        
        # result = renderers.render('temp.pt', {})
        
        # self.config = testing.setUp()
        
        # Over arching transaction
        # DBSession.execute("BEGIN")
        
        with transaction.manager:
            DBSession.execute("""UPDATE runway_settings SET value = 'True' WHERE "name" LIKE 'runway.modules.%'""")
            DBSession.execute("""DELETE FROM runway_security_checks WHERE "user" = 1""")
            DBSession.execute("COMMIT")
        
        # print("\n\n")
        # for r in DBSession.execute("SELECT * FROM runway_settings WHERE name = 'runway.modules.wordy'"):
        #     print(r)
        # print("\n\n")
        
        triggers_f._triggers_enabled = False
    
    def tearDown(self):
        DBSession.execute("ROLLBACK")
        self.session.remove()
        
        triggers_f._triggers_enabled = True
    
    def get_auth(self, testapp, auth="root"):
        # If we've no auth we just return an un-auth'd app
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
        
        # print("\n\n")
        # print(type(testapp))
        # print(dir(testapp))
        # print(testapp.cookies)
        # print(testapp.cookiejar)
        # print("\n\n")
        
        # Return the app and cookies for auth
        return testapp
        
    def make_request(self, app, path, msg="", data={}, expect_forward=False, allow_graceful=[], expect_exception="", auth="root"):
        data.update(app.cookies)
        
        return self.check_request_result(
            r                = app.get(path, data),
            path             = path,
            data             = data,
            msg              = msg,
            expect_forward   = expect_forward,
            allow_graceful   = allow_graceful,
            expect_exception = expect_exception,
        )
    
    def make_view(self, app, view, matchdict={}, params={}, msg="", request=None):
        if request is None:
            request = DummyRequest()
        
        request.matchdict = matchdict
        request.params = params
        return view(request)
    
    def get_app(self, auth="root"):
        app = main({
            '__file__': '/tmp/a',
            # 'here': '/var/www/wsgi_dev/venustate'
        }, **{
            'pyramid.includes': '\npyramid_tm',
            'sqlalchemy.url': engine_str,
            'pyramid.debug_authorization': 'false',
            'pyramid.default_locale_name': 'en',
            'pyramid.debug_notfound': 'false',
            'pyramid.debug_routematch': 'false',
            'testing_mode': "True",
            'ignore_folder': "True",
        })
        
        testapp = TestApp(app, cookiejar=http.cookiejar.CookieJar())
        return self.get_auth(testapp, auth)
    
    def check_request_result(self, r, msg="", path="", data={}, expect_forward=False, allow_graceful=[], expect_exception=""):
        # Check for traceback
        
        # if msg == "": raise Exception("No msg")
        
        if "<!-- testing flag:404.pt -->" in r:
            user_id = None
            '''
            print("\n\n")
            print(data['auth_tkt'])
            print(data['auth_tkt'].split("!"))
            print(data['auth_tkt'].split("!")[0])
            print("\n\n")
            
            user_id = int(data['auth_tkt'].split("!")[0][41:])
            auth_u = DBSession.query(User).filter(User.id == user_id).first()
            '''
            
            self.fail("""This page could not be found:

Path: {path}
ID: {user_id}
Name: {name}

Msg: {msg}""".format(
                path = path,
                user_id = user_id,
                name = "X",#auth_u.username,
                msg = msg,
            ))
        
#         # If we expect an exception and don't get one, we fail
#         if (expect_exception != "" and len(allow_graceful) == 0):
#             if errors_f.traceback_info in r:
#                 self.fail("""An exception was expected and not found:

# Path: {path}
# Msg: {msg}""".format(
#                     path = path,
#                     msg = msg,
#                 ))
            
        # We found an error!
        if errors_f.traceback_info in r:
            # Is it a graceful error?
            failure_handled = False
            exception_str = ""
            
            # First we get the exception message itself
            if "<!-- start_graceful_message -->" in str(r):
                exception_re = find_graceful.search(str(r))
                
                if exception_re != None:
                    exception_str = exception_re.groups()[0].strip()
                
                if isinstance(allow_graceful, str):
                    allow_graceful = [allow_graceful]
                
                # If the graceful message is in the allowed messages, we
                # won't fail this test
                if exception_str in allow_graceful:
                    failure_handled = True
                
                elif exception_str.strip() == expect_exception.strip():
                    failure_handled = True
            
            else:
                # It's not a graceful exception
                exception_re = find_exception.search(str(r))
                
                if exception_re != None:
                    exception_str = exception_re.groups()[0].strip()
                
                if exception_str.strip() == expect_exception.strip():
                    failure_handled = True
            
            # Now, do we fail?
            if not failure_handled:
                trace_str = find_error.search(str(r))
                if trace_str != None:
                    trace_str = trace_str.groups()[0]
                else:
                    trace_str = errors_f.cache['traceback']
                
                # if it's a graceful error, lets get the message for it
                if exception_str != "":
                    trace_str += exception_str
                
                self.fail("""
Trace: {trace}
Path: {path}
Msg: {msg}""".format(
                    trace = trace_str,
                    path = path,
                    msg = msg,
                ))
        
        # Forbidden
        if "<!-- testing flag:forbidden.pt -->" in r and expect_exception != "forbidden":
            user_id = int(data['auth_tkt'].split("!")[0][41:])
            auth_u = DBSession.query(User).filter(User.id == user_id).first()
            
            self.fail("""You do not have permission to view this page:

Path: {path}
ID: {user_id}
Name: {name}

Msg: {msg}""".format(
                path = path,
                user_id = user_id,
                name = auth_u.username,
                msg = msg,
            ))
        
        # Expect forbidden but don't get it
        if "<!-- testing flag:forbidden.pt -->" not in r and expect_exception == "forbidden":
            user_id = int(data['auth_tkt'].split("!")[0][41:])
            auth_u = DBSession.query(User).filter(User.id == user_id).first()
            
            self.fail("""Expected a forbidden page but did not find one:

Path: {path}
ID: {user_id}
Name: {name}

Msg: {msg}""".format(
                path = path,
                user_id = user_id,
                name = auth_u.username,
                msg = msg,
            ))
        
        # 302 Forwarder
        if str(r).split("\n")[0] == "Response: 302 Found":
            new_location = str(r).split("\n")[2].replace("Location: http://localhost", "")
            
            if hasattr(expect_forward, "search"):
                result = expect_forward.search(new_location)
                if result != None:
                    expect_forward, new_location = "True", "True"
            
            if expect_forward != False:
                if expect_forward == new_location:
                    return
                else:
                    # We want to save the patten
                    if hasattr(expect_forward, "search"):
                        expect_forward = "r'%s'" % expect_forward.pattern
                    else:
                        expect_forward = "'%s'" % expect_forward
                    
                    self.fail("""You have not been forwarded to the expected location.

New location: '{new_location}'
Expected location: {expect_forward}
Message: {msg}""".format(
                        new_location = new_location,
                        expect_forward = expect_forward,
                        msg = msg,
                    ))
            
            # No login details? Of course we were forwarded!
            if 'auth_tkt' not in data:
                self.fail("""You have been forwarded, no login details are in the cookie data sent to the page.

New location: {new_location}""".format(new_location = new_location))
            
            # We have login details yet are still forwarded
            # user_id = int(data['auth_tkt'].split("!")[0][41:])
            # auth_u = DBSession.query(User).filter(User.id == user_id).first()
            
            self.fail("""You have been forwarded

New location: {new_location}

ID: {user_id}
Name: {name}
""".format(
                new_location = str(r).split("\n")[2],
                user_id = None,#user_id,
                name = None,#auth_u.username,
            ))
        
        return r

# def quick_test(func, tries=100, conditions=[], *arguments):
#     plist, generators = [], []
#     for row in arguments:
#         low, high, options = None, None, {}
        
#         if type(row) not in (list, tuple): t = row
#         elif len(row) == 1: t = row[0]
#         elif len(row) == 2: t, low = row[0:2]
#         elif len(row) == 3: t, low, high = row[0:3]
#         elif len(row) == 4: t, low, high, options = row[0:4]
        
#         initial, f = test_values(t, low, high, **options)
#         plist.append(initial)
#         generators.append(f())
    
#     def attempt(*args):
#         try:
#             func(*args)
#         except Exception:
#             print(args)
#             raise
    
#     for p in itertools.product(*plist):
#         # Ensure all conditionals are satisfied
#         if False in [c(*p) for c in conditions]: continue
#         attempt(*p)
    
#     r = 0
#     while r < tries:
#         args = [g.__next__() for g in generators]
#         if False in [c(*p) for c in conditions]: continue
#         attempt(*args)
#         r += 1

# def test_values(t, low=None, high=None, **options):
#     if t == int: return _int_test(low, high, **options)
#     if t == datetime: return _datetime_test(low, high, **options)
#     else:
#         raise Exception("No handler for type of %s" % t)

# def _int_test(low=None, high=None, values=[], **options):
#     if low is None: low = -sys.maxsize
#     if high is None: high = sys.maxsize
#     initial = [low, high]
#     if low < 0 and high > 0: initial.append(0)
    
#     def f():
#         while True:
#             yield random.randint(low, high)
    
#     return initial, f

# def _datetime_test(low=None, high=None, **options):
#     now = datetime.now()
#     if low is None: low = datetime(year=1, month=1, day=1)
#     if high is None: high = datetime(year=3000, month=12, day=31)
#     initial = [low, high]
#     if low < now and high > now: initial.append(now)
    
#     def f():
#         diff = (high - low).total_seconds()
#         while True:
#             seconds = random.randint(0, diff)
#             yield low + timedelta(seconds=seconds)
#     return initial, f