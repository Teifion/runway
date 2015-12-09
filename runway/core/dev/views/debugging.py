from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
from ..lib import exceptions_f, debugging
from ...system.models import ExceptionLog
from ...system.models.user import User
from ...system.lib import user_f, render_f
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

def test_page(request):
    """
    Designed for editing and testing without having to create a new page
    """
    
    request.add_documentation("dev.home")
    
    request.render['left-dropdowns'] = [
        render_f.dropdown_menu("Block menu", "block", "fa-power-off", "", "", (
            render_f.dropdown_menu_item("Item 1", "yesterday", "fa-newspaper", "lorem ipsum loads of bacon is really really tasty and I love the smell of bacon", "?url=left-dropdowns.block.item1"),
            render_f.dropdown_menu_item("Item 2", "2 days ago", "fa-house", "lorem ipsum", "?url=left-dropdowns.block.item2"),
        )),
        render_f.dropdown_menu("Inline menu", "inline", "fa-power-off", "danger", "2", (
            render_f.dropdown_menu_item("Item 1", "yesterday", "fa-newspaper", "lorem ipsum loads of bacon is really really tasty and I love the smell of bacon", "?url=left-dropdowns.inline.item1"),
            render_f.dropdown_menu_item("Item 2", "2 days ago", "fa-home", "lorem ipsum", "?url=left-dropdowns.inline.item2"),
        )),
    ]
    
    request.render['right-dropdowns'] = [
        render_f.dropdown_menu("Status updates", "bars", "fa-power-off", "", "", (
            render_f.dropdown_menu_item("Item 1", "One hour", "danger", "60", "?url=bars1"),
            render_f.dropdown_menu_item("Item 2", "Three hours", "success", "80", "?url=bars2"),
        )),
    ]
    
    request.render['user-links'] = [
        render_f.dropdown_menu_item("Link 1", "", "home", "", "?url=user-link1"),
        render_f.dropdown_menu_item("Link 2", "", "plane", "", "?url=user-link2"),
    ]
    
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title       = 'Test page',
        layout      = layout,
        pre_content = pre_content,
    )
