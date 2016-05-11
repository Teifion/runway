from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
from ..lib import exceptions_f, debugging
from ...system.models import ExceptionLog
from ...system.models.user import User
from ...system.lib import user_f, render_f
from collections import defaultdict
import json

def slow_pages(request):
    request.do_not_log = True
    
    data   = debugging.get_slow_pages()
    
    layout = common.render("viewer")
    
    return dict(
        title       = 'Slow pages',
        layout      = layout,
        data        = data,
    )

def slow_drilldown(request):
    request.do_not_log = True
    path = request.params['path']
    
    overview = debugging.get_slow_pages(path).first()
    logs = debugging.get_logs(path)
    
    layout      = common.render("viewer")
    
    return dict(
        title       = 'Slow pages drilldown',
        layout      = layout,
        overview    = overview,
        logs        = logs,
    )

def permissions(request):
    request.do_not_log = True
    
    layout      = common.render("viewer")
    
    groups = defaultdict(list)
    for p in request.user.permissions():
        g = p.split(".")[0]
        
        groups[g].append(p)
    
    keys = list(groups.keys())
    keys.sort()
    
    return dict(
        title  = 'Permissions list',
        layout = layout,
        
        groups = groups,
        keys   = keys,
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
    
    request.render['dropdowns'] = [
        render_f.dropdown_menu("Block menu", "block", "fa-power-off", "", "", (
            render_f.dropdown_menu_item("Item 1", "yesterday", "fa-newspaper", "lorem ipsum loads of bacon is really really tasty and I love the smell of bacon", "?url=left-dropdowns.block.item1", label_colour="warning", label_text="Warn"),
            render_f.dropdown_menu_item("Item 2", "2 days ago", "fa-home", "lorem ipsum", "?url=left-dropdowns.block.item2"),
            render_f.dropdown_menu_item("Lots of text", "3 days ago", "fa-bullhorn", """
                Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
                cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
                proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                """, "?url=left-dropdowns.block.item3", label_colour="danger", label_text="danger"),
        )),
        render_f.dropdown_menu("Inline menu", "inline", "fa-power-off", "danger", "2", (
            render_f.dropdown_menu_item("Item 1", "yesterday", "fa-newspaper-o", "lorem ipsum loads of bacon is really really tasty and I love the smell of bacon", "?url=left-dropdowns.inline.item1"),
            render_f.dropdown_menu_item("Item 2", "2 days ago", "fa-home", "lorem ipsum", "?url=left-dropdowns.inline.item2"),
            render_f.dropdown_menu_item("Item 3", "8 days ago", "fa-exclamation", "Ipsum lorem something or other", "?url=left-dropdowns.inline.item3", "danger", "danger label"),
        )),
        render_f.dropdown_menu("Grid", "grid", "fa-th", "success", "", (
            # "title", "muted_text", "icon", "body", "url", "label_colour", "label_text"
            
            render_f.dropdown_menu_item("Item 1", "", "fa-bank", "", "?url=left-dropdowns.grid.item1", "success"),
            render_f.dropdown_menu_item("Item 2", "", "fa-newspaper-o", "", "?url=left-dropdowns.grid.item1", "primary"),
            render_f.dropdown_menu_item("Item 3", "", "fa-power-off", "", "?url=left-dropdowns.grid.item1", "danger"),
            render_f.dropdown_menu_item("Item 4", "", "fa-cc", "", "?url=left-dropdowns.grid.item1", "warning"),
            render_f.dropdown_menu_item("Item 5", "", "fa-history", "", "?url=left-dropdowns.grid.item1", "success"),
            render_f.dropdown_menu_item("Item 6", "", "fa-anchor", "", "?url=left-dropdowns.grid.item1", "primary"),
            render_f.dropdown_menu_item("Item 7", "", "fa-deafness", "", "?url=left-dropdowns.grid.item1", "warning"),
            render_f.dropdown_menu_item("Item 8", "", "fa-map-pin", "", "?url=left-dropdowns.grid.item1", "danger"),
            render_f.dropdown_menu_item("Item 9", "", "fa-suitcase", "", "?url=left-dropdowns.grid.item1", "success"),
        )),
        render_f.dropdown_menu("Status updates", "bars", "fa-power-off", "", "", (
            render_f.dropdown_menu_item("Item 1", "One hour", "danger", "60", "?url=bars1"),
            render_f.dropdown_menu_item("Item 2", "Three hours", "warning", "80", "?url=bars2"),
            render_f.dropdown_menu_item("Item 3", "Done", "success", "100", "?url=bars3"),
        )),
    ]
    
    request.render['user_links'] = [
        render_f.dropdown_menu_item("Link 1", "", "home", "Body 1", "?url=user-link1"),
        render_f.dropdown_menu_item("Link 2", "", "plane", "Body 2", "?url=user-link2"),
    ]
    
    layout      = common.render("viewer")
    
    return dict(
        title       = 'Test page',
        layout      = layout,
    )
