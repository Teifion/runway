from pyramid.httpexceptions import HTTPFound
from ....core.lib import common
from ....core.system.lib import user_f

def home(request):
    layout      = common.render("viewer")
    
    stories = []
    
    return dict(
        title   = "News",
        layout  = layout,
        
        stories = stories,
    )

def control_panel(request):
    layout      = common.render("viewer")
    
    stories = []
    
    return dict(
        title   = "News",
        layout  = layout,
        
        stories = stories,
    )
