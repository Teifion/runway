from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
from ..lib import exceptions_f
from ...system.models import ExceptionLog
from ...system.models.user import User
from ...system.lib import user_f
import json

def list_exceptions(request):
    assigned = int(request.params.get('assigned', -1))
    if assigned == -1: assigned = None
    
    show_all = request.params.get("all", "") == "true"
    exception_list = exceptions_f.exception_list(user_id=assigned, show_all=show_all)
    
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title          = 'Exception list',
        layout         = layout,
        pre_content    = pre_content,
        exception_list = exception_list,
    )

def edit(request):
    exception_id = int(request.matchdict['exception_id'])
    the_exception = exceptions_f.get_exception(exception_id)
    
    if the_exception.user != None:
        the_user = user_f.get_user(the_exception.user)
    else:
        # This gets the guest account
        the_user = user_f.get_user(2)
    
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title          = 'Edit exception: %d' % the_exception.id,
        layout         = layout,
        pre_content    = pre_content,
        the_exception  = the_exception,
        the_user       = the_user,
        common         = common,
        exception_data = json.loads(the_exception.data),
    )

def hide(request):
    exception_id = int(request.matchdict['exception_id'])
    
    exceptions_f.hide_exception(exception_id)
    return HTTPFound(location = request.route_url("dev.exception.list"))

def hide_all(request):
    exceptions_f.hide_all_exceptions()
    return HTTPFound(location = request.route_url("dev.exception.list"))
