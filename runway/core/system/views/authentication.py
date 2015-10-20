from pyramid.httpexceptions import HTTPFound

from pyramid.security import (
    remember,
    forget,
)

from pyramid.renderers import get_renderer

# from ... import security

from ...lib import common
from ..lib import user_f, security, site_settings_f

login_redirect_url = "core.login"

def forbidden(request):
    if not hasattr(request, "user") or request.user.id == 2:
        path = request.path
        
        if path == "/logout":
            path = ""
        
        return HTTPFound(location = "{}?redirect={}".format(
            request.route_url(login_redirect_url),
            common.encode(redirect=path)
        ))
    
    layout = common.render("blank")
    
    return dict(
        title = "503: No access permission",
        layout = layout
    )

def login(request):
    request.do_not_log = True
    layout = common.render("blank")
    
    redirect = request.params.get("redirect", "")
    if redirect != "":
        try:
            redirect = common.decode(redirect)[1]['redirect']
        except Exception:
            redirect = "/"
        
    else:
        redirect = "/"
    
    # If no redirect or default redirect, we want to look at maybe sending them back where
    # they came from
    if redirect == "/":
        login_url = request.route_url('core.login')
        referrer = request.url
        if referrer == login_url:
            # never use the login form itself as came_from
            referrer = request.route_url('/')
        came_from = request.params.get('came_from', referrer)
        redirect = came_from
    
    message  = None
    partial  = None
    username = ''
    
    if 'username' in request.params:
        user_id, result = security.login(request)
        
        if user_id == "failure":
            message = "danger", result
        
        elif result in ("complete", None):
            # They're in? Best do stuff then!
            return security.successful_login(request, user_id, redirect)
            
            # user_f.update_session_ip(user_id, session_ip=request.remote_addr)
            # headers = remember(request, user_id, max_age = 60*60*24*7*9999)
            # return HTTPFound(location = came_from, headers = headers)
        else:
            # They have partials, we better do something about that
            return HTTPFound(location=request.route_url('core.login') + "?h=" + result)
    
    if 'h' in request.params:
        partial = security.perform_partial(request)
        if isinstance(partial, HTTPFound):
            return partial
        
        if 'message' in partial:
            message = partial['message']
    
    return dict(
        title     = "Login",
        redirect  = redirect,
        message   = message,
        login     = username,
        # url       = request.route_url('core.login'),
        layout    = layout,
        partial   = partial,
        
        allow_registration = site_settings_f.get_setting("runway.users.allow_registration", False) == "True",
    )

def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('core.login'), headers = headers)

def external_auth(request):
    layout = common.render("blank")
    
    message = ""
    
    return dict(
        title   = "External login",
        layout  = layout,
        message = message,
    )
