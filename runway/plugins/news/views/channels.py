from pyramid.httpexceptions import HTTPFound
from ....core.lib import common
from ....core.system.lib import user_f

def add(request):
    layout      = common.render("viewer")
    
    return dict(
        title       = "Page title",
        layout      = layout,
    )