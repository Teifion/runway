from pyramid.httpexceptions import HTTPFound
from ....core.lib import common
from ....core.system.lib import user_f
from ..lib import channels_f

def home(request):
    layout      = common.render("viewer")
    
    channels = channels_f.get_channels(None, "owner")
    
    return dict(
        title    = "News admin",
        layout   = layout,
        
        channels = channels,
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
        title    = "Edit channel",
        layout   = layout,
    )

    
def delete_channel(request):
    layout      = common.render("viewer")
    
    return dict(
        title    = "Delete channel",
        layout   = layout,
    )


