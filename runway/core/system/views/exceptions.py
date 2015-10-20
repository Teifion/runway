import traceback
import json
import sys
import re
from sqlalchemy import func
from pyramid.view import view_config

from pyramid.security import unauthenticated_userid

from pyramid.httpexceptions import HTTPFound

from ...base import DBSession
from ..models.user import User
from ..models import ExceptionLog

import traceback
import transaction
import sqlalchemy
from ...lib import common
from ..lib import errors_f, site_settings_f
import sys

_graceful_errors = (
    (
        re.compile(r"time data '[^']+' does not match format '%Y-%m-%d'"),
        ("Time error", lambda x: x, "Input")
    ),
)

# Exceptions can't use the normal permission requirement
# so the request is never passed through the security
# function that's assigning request.user
def get_user_object(request, user_id=2):
    userid = unauthenticated_userid(request)
    if userid is not None:
        the_user = DBSession.query(User).filter(User.id == userid).first()
        request.user = the_user
    else:
        # Set ID to that of guest
        request.user = User(id=user_id)
        request.user.init_on_load()

def general_exception(exc, request):
    get_user_object(request)
    
    layout = common.render("viewer")
    pre_content = common.render("general_menu")
    
    exc._runway_log_flag = True
    
    for regex, (title, body_func, category) in _graceful_errors:
        if regex.search(exc.args[0]):
            exc.title = title
            exc.message = body_func(exc.args[0])
            exc._runway_log_flag = False
    
    if not hasattr(exc, "message"):
        exc.message = "There has been a general exception in the program."
    
    if not hasattr(exc, "title"):
        exc.title = "Unexpected error"
    
    # This is to prevent us showing a traceback on live pages
    traceback_str = ""
    if "testing_mode" in request.registry.settings:
        traceback_str = traceback.format_exc()
    
    # This prints out the traceback if we're accessing it on the default
    # dev port
    if request.host[-5:] == ":6543":
        etype, evalue, etb = sys.exc_info()
        print('\n\n')
        print(''.join(traceback.format_exception(etype, evalue, etb)))
        print('\n\n')
    
    if exc._runway_log_flag:
        html_traceback = errors_f.log_error(exc, request)
    else:
        html_traceback = errors_f.html_render(sys.exc_info(), context=5, request=request)
    
    return dict(
        title          = exc.title,
        layout         = layout,
        pre_content    = pre_content,
        message        = exc.message,
        html_traceback = html_traceback,
        traceback      = traceback_str,
        exc            = exc,
        dev_email      = site_settings_f.get_setting("runway.system.dev_email"),
    )

def not_found_exception(exc, request):
    layout = common.render("viewer")
    pre_content = common.render("general_menu")
    
    request.do_not_log = True
    get_user_object(request)
    
    return dict(
        title    = 'Page not found',
        message  = "404",
        layout   = layout,
        pre_content = pre_content,
    )

def display_graceful_exception(exc, request):
    get_user_object(request)
    
    if exc.log_anyway:
        errors_f.log_error(sys.exc_info(), request)
    
    layout = common.render("viewer")
    pre_content = common.render("general_menu")
    
    if exc.category not in errors_f.graceful_images:
        fail_image = errors_f.graceful_images['default']
    else:
        fail_image = errors_f.graceful_images[exc.category]
    
    return dict(
        title      = exc.title,
        layout     = layout,
        pre_content = pre_content,
        exc        = exc,
        fail_image = fail_image,
    )

# def ajax_error_count(request):
#     request.do_not_log = True
    
#     c = DBSession.query(func.count(ExceptionLog.id)).filter(ExceptionLog.fixed == False).first()
#     return 0 if c == None else c[0]

def dbapi_error(exc, request):
    get_user_object(request)
    
    layout = common.render("viewer")
    pre_content = common.render("general_menu")
    
    # Extra info for debugging
    try:
        dir_dump = "\n".join(common.dumps(exc, print_string=False))
    except Exception as e:
        dir_dump = "Error trying to dump the object: {}".format(str(e.args))
    
    dir_dump = "<br />EXTRA DEBUG INFO:<br /><pre>dir(exc): {}</pre>".format(dir_dump)
    
    exc._runway_log_flag = True
    
    for regex, (title, body_func, category) in _graceful_errors:
        if regex.search(exc.args[0]):
            exc.title = title
            exc.message = body_func(exc.args[0])
            exc._runway_log_flag = False
    
    if not hasattr(exc, "message"):
        exc.message = "There has been a general exception in the program."
    
    if not hasattr(exc, "title"):
        exc.title = "Unexpected error"
    
    # This is to prevent us showing a traceback on live pages
    traceback_str = ""
    if "testing_mode" in request.registry.settings:
        traceback_str = traceback.format_exc()
    
    # This prints out the traceback if we're accessing it on the default
    # dev port
    if request.host[-5:] == ":6543":
        etype, evalue, etb = sys.exc_info()
        print('\n\n')
        print(''.join(traceback.format_exception(etype, evalue, etb)))
        print('\n\n')
    
    if exc._runway_log_flag:
        html_traceback = errors_f.log_error(exc, request)
    else:
        html_traceback = errors_f.html_render(sys.exc_info(), context=5, request=request, extra_html=dir_dump)
    
    return dict(
        title          = exc.title,
        layout         = layout,
        pre_content    = pre_content,
        message        = exc.message,
        html_traceback = html_traceback,
        traceback      = traceback_str,
        exc            = exc,
        dev_email      = site_settings_f.get_setting("runway.system.dev_email"),
    )

def deactivated_user(request):
    layout = common.render("blank")
    
    return dict(
        title = "Deactivated user",
        layout = layout
    )
