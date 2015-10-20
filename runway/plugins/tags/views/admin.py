from pyramid.httpexceptions import HTTPFound
from ....core.lib import common
from ....core.system.lib import user_f

def home(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title       = "Page title",
        layout      = layout,
        pre_content = pre_content,
    )
