from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
from ..lib import funcs

def list_hooks(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    hooks = list(funcs._hook_info.keys())
    hooks.sort()
    
    return dict(
        title       = "Developer: Hooks",
        layout      = layout,
        pre_content = pre_content,
        
        hooks     = [(h, funcs._hook_info[h]) for h in hooks],
    )
