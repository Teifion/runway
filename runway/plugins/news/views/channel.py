from pyramid.httpexceptions import HTTPFound
from ....core.lib import common
from ....core.system.lib import user_f


    
def view(request):
    layout      = common.render("viewer")
    
    return dict(
        title       = "Edit item",
        layout      = layout,
        
        the_item = the_item,
    )

    
def search(request):
    layout      = common.render("viewer")
    
    return dict(
        title       = "Edit item",
        layout      = layout,
        
        the_item = the_item,
    )

    
def subscribe(request):
    layout      = common.render("viewer")
    
    return dict(
        title       = "Edit item",
        layout      = layout,
        
        the_item = the_item,
    )

    
def unsubscribe(request):
    layout      = common.render("viewer")
    
    return dict(
        title       = "Edit item",
        layout      = layout,
        
        the_item = the_item,
    )
