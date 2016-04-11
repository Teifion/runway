from pyramid.httpexceptions import HTTPFound
from ....core.lib import common
from ....core.system.lib import user_f
from ..lib import channels_f
from ..models import NewsChannel

def home(request):
    layout      = common.render("viewer")
    
    channels = channels_f.get_channels(None, "owner")
    
    return dict(
        title    = "News admin",
        layout   = layout,
        
        channels = channels,
    )

#  CHANNELS
def new_channel(request):
    layout      = common.render("viewer")
    
    if request.params.get("channel_name","").strip() != "":
        channel_name = request.params.get("channel_name","").strip()
        sys_name = channel_name.replace(" ", "_")
        
        the_channel = NewsChannel(
            sys_name      = sys_name,
            name          = channel_name,
            
            description   = request.params.get("description","").strip(),
            permissions   = "",
            
            owner         = request.user.id,
        )
        
        channels_f.add_channel(the_channel)
        return HTTPFound(request.route_url("news.admin.home"))
    
    return dict(
        title    = "New channel",
        layout   = layout,
    )

    
def edit_channel(request):
    layout      = common.render("viewer")
    
    channel_id = int(request.matchdict['channel_id'])
    the_channel = channels_f.get_channel(channel_id)
    
    if request.params.get("channel_name","").strip() != "":
        pass
    
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


#  ITEMS
def new_item(request):
    layout      = common.render("viewer")
    
    return dict(
        title    = "TODO",
        layout   = layout,
    )

def edit_item(request):
    layout      = common.render("viewer")
    
    return dict(
        title    = "TODO",
        layout   = layout,
    )

def delete_item(request):
    layout      = common.render("viewer")
    
    return dict(
        title    = "TODO",
        layout   = layout,
    )
