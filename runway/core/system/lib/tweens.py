import re
import os
from datetime import datetime
from time import time
import transaction

from pyramid.httpexceptions import HTTPFound
from ...base import DBSession

from ..models import ViewLog
from . import site_settings_f
from ...documentation.lib import docs_f
from ...lib import common
from ..views.exceptions import get_user_object
from collections import defaultdict

from ....core.hooks.lib.funcs import call_hook

ignored_filetypes = re.compile(r"(css|js|html|png|jpg|jpeg|ico|gif|woff)$")
no_section_grep = re.compile(r"^/([a-zA-Z0-9_]+)/[a-zA-Z0-9_]+$")
section_grep = re.compile(r"(?:/[a-zA-Z]+)?/([a-zA-Z0-9_]+?)/")
local_section_grep = re.compile(r"([a-zA-Z0-9_]+?)/")

def test_tween_skip(request):
    if request.environ['PATH_INFO'][:8] == "/static/":
        return True
    
    if request.environ['PATH_INFO'][:8] == "/favicon":
        return True
    
    return False

def make_rel(request):
    l = len(request.path.split("/"))
    def rel(link):
        return "{}/{}".format("/".join([".."]*(max(0, l-2))), link)
    return rel

def logging_tween_factory(handler, registry):
    """
    This is the tween which logs error messages.
    """
    def logging_tween(request):
        if test_tween_skip(request):
            request.anonymous = False
            return handler(request)
        
        if ignored_filetypes.search(request.path.strip()):
            request.anonymous = False
            return handler(request)
        
        if not hasattr(request, "user"):
            get_user_object(request, user_id=2)
            
            if not request.user.active and request.user.id != 2:
                if "/exceptions/deactivated_user" not in request.path and "/logout" not in request.path and "/login" not in request.path:
                    return HTTPFound(location=request.route_url('exceptions.deactivated_user'))
        
        request.rel = make_rel(request)
        
        request.do_not_log = False
        request.anonymous  = False
        request.user_log   = ViewLog()
        
        # Handle
        start = time()
        response = handler(request)
        
        if getattr(request, "api_bypass_tweens", False) == True:
            return response
        
        # TODO
        # This was erroring with the API calls and it looks
        # like the request.user_log is never actually referenced
        # try:
        #     response = handler(request)
        # finally:
        #     if hasattr(request, "user"):
        #         request.user_log.user = request.user.id
        #     else:
        #         request.user_log.user = None
        
        # If it's a forward we don't want to log it
        for h in response.headerlist:
            if h[0] == "Location":
                request.do_not_log = True
        
        u = None
        if hasattr(request, "user"):
            if request.user.id > 0:
                u = request.user.id
        
        # Now maybe log
        if not request.do_not_log:
            if request.anonymous or u is None:
                u = 2
            
            section = ""
            if request.host[-5:] != ":6543" or True:
                r = no_section_grep.search(request.path)
                if r is None:
                    r = section_grep.search(request.path)
            else:
                r = local_section_grep.search(request.path)
            
            if r != None:
                section = r.groups()[0]
            
            with transaction.manager:
                stmt = """INSERT INTO runway_logs
                ("timestamp", "path", "user", "load_time", "section", "ip") VALUES
                (:timestamp, :path, :user, :load_time, :section, :ip);"""
                
                args = dict(
                    timestamp = datetime.today(),
                    path      = request.path.replace("'", "''"),
                    section   = section,
                    user      = u,
                    load_time = time() - start,
                    ip        = request.remote_addr if request.remote_addr != None else '',
                )
                
                # For some reason it won't let us use DBSession.add()
                DBSession.execute(stmt, args)
                DBSession.execute("COMMIT")
            
            # print("\n\n---\n")
            # print("\n5\n")
            
        return response
        
    return logging_tween

def settings_tween_factory(handler, registry):
    def settings_tween(request):
        if test_tween_skip(request):
            request.runway_settings = defaultdict(dict)
            return handler(request)
        
        request.runway_settings = site_settings_f._settings_collection
        return handler(request)
        
    return settings_tween


def _adder(request, attr):
    the_attr = getattr(request, attr)
    def f(value):
        if value not in the_attr:
            the_attr.append(value)
            
    return f

def render_tween_factory(handler, registry):
    def render_tween(request):
        request._js_libs     = []
        request._css_libs    = []
        
        request._js_raws     = []
        request._css_raws    = []
        
        request._html_raws   = []
        
        if test_tween_skip(request):
            return handler(request)
        
        request.add_js_lib   = _adder(request, "_js_libs")
        request.add_css_lib  = _adder(request, "_css_libs")
        request.add_js_raw   = _adder(request, "_js_raws")
        request.add_css_raw  = _adder(request, "_css_raws")
        request.add_html_raw = _adder(request, "_html_raws")
        
        return handler(request)
        
    return render_tween


def menu_tween_factory(handler, registry):
    def menu_tween(request):
        request._documentation = []
        request.render = defaultdict(dict)
        
        if test_tween_skip(request):
            request.get_docs = lambda: []
            return handler(request)
        
        if not hasattr(request, "user"):
            permissions = []
        else:
            permissions = request.user.permissions()
        
        site_menu = []
        for sm in site_settings_f._hidden_settings['site_menu'].values():
            if all(req in permissions for req in sm['permissions']):
                site_menu.append(sm)
        
        
        request.render["site_menu"] = site_menu
        request.render["user_links"] = []
        request.render["documentation"] = []
        
        # request.add_documentation = _adder(request, "_documentation")
        request.add_documentation = request.render["documentation"].append
        request.get_docs = lambda: (docs_f._docs[d] for d in request.render["documentation"])
        request.is_documentation = False
        
        call_hook("pre_render", request=request)
        
        return handler(request)
        
    return menu_tween
