from pyramid.httpexceptions import HTTPFound
from ....core.lib import common
from ....core.system.lib import user_f, logs_f
from ..lib import channels_f, items_f
from ..models import Channel, Item
from ....core.system.js_widgets import UserPicker
from ....core.system.lib import site_settings_f, user_settings_f
from datetime import datetime, timedelta

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
        
        the_channel = Channel(
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
        channel_name = request.params.get("channel_name","").strip()
        sys_name = channel_name.replace(" ", "_")
        
        # Set attributes
        the_channel.sys_name      = sys_name
        the_channel.name          = channel_name
        
        the_channel.hidden        = "hidden" in request.params
        
        the_channel.description   = request.params.get("description","").strip()
        
        channels_f.add_channel(the_channel)
        return HTTPFound(request.route_url('news.admin.channel.edit', channel_id=the_channel.id))
    
    channel_items = items_f.get_items(the_channel.id, "poster")
    subscriptions = channels_f.get_subscriptions(the_channel.id, get_users=True)
    
    return dict(
        title         = "Edit channel",
        layout        = layout,
        
        the_channel   = the_channel,
        channel_items = channel_items,
        subscriptions = subscriptions,
    )

    
def delete_channel(request):
    layout   = common.render("modal")
    
    channel_id = int(request.matchdict['channel_id'])
    the_channel = channels_f.get_channel(channel_id)
    
    if the_channel != None and request.params.get('confirm') == 'confirm':
        logs_f.audit_log(request, request.user.id, "news.admin.channel.delete", """Channel #{channel} deleted
Name: {name}
SysName: {sys_name}
Owner: {owner}
""".format(
            channel  = the_channel.id,
            name     = the_channel.name,
            sys_name = the_channel.sys_name,
            hidden   = the_channel.hidden,
            owner    = the_channel.owner,
        ))
        
        channels_f.delete_channel(the_channel)
        the_channel = None
        
        
    
    return dict(
        title    = "Delete channel",
        layout   = layout,
        
        the_channel = the_channel,
    )

def hide_channel(request):
    channel_id = int(request.matchdict['channel_id'])
    the_channel = channels_f.get_channel(channel_id)
    
    the_channel.hidden = True
    
    return HTTPFound(request.route_url('news.admin.channel.edit', channel_id=the_channel.id))


def add_subscription(request):
    channel_id = int(request.matchdict['channel_id'])
    user_id = int(request.matchdict['user_id'])
    
    channels_f.add_subscriptions(channel_id, user_id)
    
    return HTTPFound(request.route_url('news.admin.channel.edit', channel_id=channel_id))
    
def remove_subscription(request):
    channel_id = int(request.matchdict['channel_id'])
    user_id = int(request.matchdict['user_id'])
    
    channels_f.remove_subscriptions(channel_id, user_id)
    
    return HTTPFound(request.route_url('news.admin.channel.edit', channel_id=channel_id))


def add_subscriptions(request):
    channel_id = int(request.matchdict['channel_id'])
    names = request.params['names']
    
    user_ids = user_f.get_userids(*names.split("\n"))
    channels_f.add_subscriptions(channel_id, *user_ids)
    
    return HTTPFound(request.route_url('news.admin.channel.edit', channel_id=channel_id))




#  ITEMS
def new_item(request):
    layout      = common.render("viewer")
    
    channel_id = int(request.params['channel_id'])
    title = request.params.get("title","").strip()
    
    if request.params.get("title","").strip() != "" and channel_id > 0:
        
        sys_name = title.replace(" ", "_")
        
        the_item = Item(
            channel       = channel_id,
            title         = title,
            icon          = "",
            content       = "",
            
            poster        = request.user.id,
            published     = None,
        )
        
        items_f.add_item(the_item)
        return HTTPFound(request.route_url("news.admin.channel.edit", channel_id=channel_id))
    else:
        raise common.GracefulException("We need a name", """
            We need a title for this item! Without it we can't create the item.
            """,
            category="input")
        
    return dict(
        title    = "New item",
        layout   = layout,
    )

def edit_item(request):
    layout      = common.render("viewer")
    
    if request.params.get("editor", "") == "raw":
        editor = "raw"
    else:
        editor = user_settings_f.get_setting(request.user.id, "news.editor")
        if editor in ("Default", None):
            editor = site_settings_f.get_setting("news.editor")
    
    item_id = int(request.matchdict['item_id'])
    the_item, the_poster = items_f.get_item(item_id, "poster")
    
    UserPicker(request)
    
    if request.params.get("title","").strip() != "":
        
        # print("\n\n")
        # print(request.params.get("content","").strip())
        # print("\n\n")
        # raise Exception("")
        
        title = request.params.get("title","").strip()
        title = title.replace(" ", "_")
        
        user_id = user_f.get_userid(request.params['poster'])
        if user_id is None:
            raise common.GracefulException("We can't find that user", "We can't find a user with the name '{}'".format(params['agent']), category="Not found")
        
        
        # Set attributes
        the_item.title     = title
        the_item.icon      = request.params.get("icon","").strip()
        the_item.content   = request.params.get("content","").strip()
        
        the_item.poster    = user_id
        # the_item.published = common.string_to_datetime(request.params["published"], default=None)
        
        items_f.add_item(the_item)
        return HTTPFound(request.route_url('news.admin.item.edit', item_id=the_item.id))
    
    item_items = items_f.get_items(the_item.id, "poster")
    
    return dict(
        title      = "Edit item",
        layout     = layout,
        
        the_item   = the_item,
        the_poster = the_poster,
        
        editor     = editor,
        cdn        = site_settings_f.get_setting("news.cdn"),
    )

def delete_item(request):
    layout      = common.render("viewer")
    
    return dict(
        title    = "TODO",
        layout   = layout,
    )

def publish_item(request):
    layout      = common.render("viewer")
    
    item_id = int(request.matchdict['item_id'])
    the_item = items_f.get_item(item_id)
    
    if "confirm" in request.params:
        the_date = request.params.get("date", "")
        
        #  Publish instantly
        if the_date == "":
            publish_date = datetime.now()
        
        # Publish at the established time
        else:
            publish_date = common.string_to_datetime("{}T{}".format(request.params['date'], request.params['time']))
        
        items_f.publish_item(the_item, publish_date)
        return HTTPFound(request.route_url('news.admin.item.edit', item_id=item_id))
    
    return dict(
        title    = "News admin: Publish item",
        layout   = layout,
        
        the_item = the_item,
        
        tomorrow = datetime.now() + timedelta(days=1),
    )
