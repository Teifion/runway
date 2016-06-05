from pyramid.httpexceptions import HTTPFound
from ....core.lib import common
from ....core.system.lib import user_f
from ..lib import items_f

def home(request):
    layout      = common.render("viewer")
    
    stories = items_f.get_items(request.user.id)
    
    
    
    http://webapplayers.com/homer_admin-v1.9/notes.html
    
    
    
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
