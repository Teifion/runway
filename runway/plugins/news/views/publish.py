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


def new_channel(request):
    layout      = common.render("viewer")
    
    return dict(
        title    = "New channel",
        layout   = layout,
    )

    
def edit_channel(request):
    layout      = common.render("viewer")
    
    return dict(
        title       = "Edit channel",
        layout      = layout,
        
        the_channel = the_channel,
    )

    
def delete_channel(request):
    layout      = common.render("viewer")
    
    return dict(
        title    = "Delete channel",
        layout   = layout,
    )





def new_item(request):
    layout      = common.render("viewer")
    
    return dict(
        title    = "New item",
        layout   = layout,
    )

    
def edit_item(request):
    layout      = common.render("viewer")
    
    return dict(
        title       = "Edit item",
        layout      = layout,
        
        the_item = the_item,
    )

    
def publish_item(request):
    layout      = common.render("viewer")
    
    return dict(
        title       = "Edit item",
        layout      = layout,
        
        the_item = the_item,
    )

def review_item(request):
    layout      = common.render("viewer")
    
    return dict(
        title       = "Edit item",
        layout      = layout,
        
        the_item = the_item,
    )

def delete_item(request):
    layout      = common.render("viewer")
    
    return dict(
        title    = "Delete item",
        layout   = layout,
    )