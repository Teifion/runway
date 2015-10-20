from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
from ..lib import exceptions_f, debugging
from ...system.models import ExceptionLog
from ...system.models.user import User
from ...system.lib import user_f
import json

def slow_pages(request):
    request.do_not_log = True
    
    data = debugging.get_slow_pages()
    
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title       = 'Slow pages',
        layout      = layout,
        pre_content = pre_content,
        data        = data,
    )

def slow_drilldown(request):
    request.do_not_log = True
    path = request.params['path']
    
    overview = debugging.get_slow_pages(path).first()
    logs = debugging.get_logs(path)
    
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title       = 'Slow pages drilldown',
        layout      = layout,
        pre_content = pre_content,
        overview    = overview,
        logs        = logs,
    )

def neighbouring_logs(request):
    request.do_not_log = True
    
    user = request.params.get("user", None)
    path = request.params.get("path", None)
    log_id = int(request.params["log_id"])
    
    return dict(
        log_id = log_id,
        logs = debugging.get_neighbouring_logs(log_id, user=user, path=path)
    )
