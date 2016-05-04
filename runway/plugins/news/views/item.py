from pyramid.httpexceptions import HTTPFound
from ....core.lib import common
from ....core.system.lib import user_f, logs_f
from ..lib import channels_f, items_f
from ..models import NewsChannel, NewsItem
from ....core.system.js_widgets import UserPicker

def view(request):
    layout      = common.render("viewer")
    
    item_id = int(request.matchdict['item_id'])
    the_item, the_poster = items_f.get_item(item_id, "poster")
    
    # If this is the first time they've looked at the item
    # then we want to log they've looked at it
    the_log = items_f.get_log(item_id, request.user.id)
    if the_log is None:
        items_f.log_view(item_id, request.user.id)
    
    return dict(
        title      = the_item.title,
        layout     = layout,
        
        the_item   = the_item,
        the_poster = the_poster,
    )


def sign(request):
    layout      = common.render("viewer")
    
    return dict(
        title    = "Signing item as read",
        layout   = layout,
    )
