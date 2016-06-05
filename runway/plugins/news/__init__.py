from ...core.system.lib import site_settings_f

route_prefix = "news"

from . import schema

site_menu = {
    "id": "news",
    "permissions": ['news'],
    "route":"news.general.home",
    "icon": "fa-newspaper-o",
    "text": "News",
    "order": 20,
    "submenu": [],
}

site_settings = [
    ["News", [
        ("news.global_visibility", "admin", "Global visibility", "boolean", "True", """Everybody will be able to see the news section as a whole. Channels can still mark themselves as private and will be hidden to those not in the relevant groups."""),
        ("news.editor", "news.admin", "Editor", "list:TinyMCE,Summernote,ACE", "Summernote", """The type of editor used to edit documents."""),
        ("news.cdn", "news.cdn", "CDN", "boolean", "False", """Do you want to use the CDN for loading of the editor. If yes it will use the cloudflare CDN (Content Delivery Network) rather than loading it from the server version. Defaults to off."""),
    ]],
]

user_settings = [
    ["News", [
        ("news.editor", True, "Editor", "list:Default,TinyMCE,Summernote,ACE", "Default", """The editor window used when writing or editing documents."""),
    ]],
]

admin_menu = (
    ("news.admin.home", "fa-newspaper-o", "News", "news.admin"),
)

def admin_views(config):
    from .views import admin
    
    config.add_route('news.admin.home', 'admin/home')
    
    config.add_route('news.admin.channel.new', 'admin/channel/new')
    config.add_route('news.admin.channel.edit', 'admin/channel/edit/{channel_id}')
    config.add_route('news.admin.channel.delete', 'admin/channel/delete/{channel_id}')
    config.add_route('news.admin.channel.hide', 'admin/channel/hide/{channel_id}')
    
    config.add_route('news.admin.channel.add_subscription', 'admin/channel/add_subscription/{channel_id}/{user_id}')
    config.add_route('news.admin.channel.remove_subscription', 'admin/channel/remove_subscription/{channel_id}/{user_id}')
    
    config.add_route('news.admin.channel.add_subscriptions', 'admin/channel/add_subscription/{channel_id}')
    
    config.add_route('news.admin.item.new', 'admin/item/new')
    config.add_route('news.admin.item.edit', 'admin/item/edit/{item_id}')
    config.add_route('news.admin.item.delete', 'admin/item/delete/{item_id}')
    config.add_route('news.admin.item.publish', 'admin/item/publish/{item_id}')
    
    config.add_view(admin.home, route_name='news.admin.home', renderer='templates/admin/home.pt', permission='news.admin')
    
    
    config.add_view(admin.new_channel, route_name='news.admin.channel.new', renderer='templates/admin/channel/new.pt', permission='news.admin')
    config.add_view(admin.edit_channel, route_name='news.admin.channel.edit', renderer='templates/admin/channel/edit.pt', permission='news.admin')
    config.add_view(admin.delete_channel, route_name='news.admin.channel.delete', renderer='templates/admin/channel/delete.pt', permission='news.admin')
    config.add_view(admin.hide_channel, route_name='news.admin.channel.hide', permission='news.admin')
    
    config.add_view(admin.add_subscription, route_name='news.admin.channel.add_subscription', permission='news.admin')
    config.add_view(admin.remove_subscription, route_name='news.admin.channel.remove_subscription', permission='news.admin')
    
    config.add_view(admin.add_subscriptions, route_name='news.admin.channel.add_subscriptions', permission='news.admin')
    
    config.add_view(admin.new_item, route_name='news.admin.item.new', renderer='templates/admin/item/new.pt', permission='news.admin')
    config.add_view(admin.edit_item, route_name='news.admin.item.edit', renderer='templates/admin/item/edit.pt', permission='news.admin')
    config.add_view(admin.delete_item, route_name='news.admin.item.delete', renderer='templates/admin/item/delete.pt', permission='news.admin')
    config.add_view(admin.publish_item, route_name='news.admin.item.publish', renderer='templates/admin/item/publish.pt', permission='news.admin')

def publish_views(config):
    from .views import publish
    
    config.add_route('news.publish.home', 'publish/home')
    
    config.add_view(publish.home, route_name='news.publish.home', renderer='templates/publish/home.pt', permission='news.publish')
    
    
    config.add_route('news.publish.channel.new', 'publish/channel/new')
    config.add_route('news.publish.channel.edit', 'publish/channel/edit/{channel_id}')
    config.add_route('news.publish.channel.delete', 'publish/channel/delete')
    
    config.add_route('news.publish.item.new', 'publish/item/new')
    config.add_route('news.publish.item.edit', 'publish/item/edit/{item_id}')
    config.add_route('news.publish.item.publish', 'publish/item/publish/{item_id}')
    config.add_route('news.publish.item.review', 'publish/item/review/{item_id}')
    config.add_route('news.publish.item.delete', 'publish/item/delete')
    
    
    config.add_view(publish.new_channel, route_name='news.publish.channel.new', renderer='templates/publish/channel/new.pt', permission='news.publish')
    config.add_view(publish.edit_channel, route_name='news.publish.channel.edit', renderer='templates/publish/channel/edit.pt', permission='news.publish')
    config.add_view(publish.delete_channel, route_name='news.publish.channel.delete', renderer='templates/publish/channel/delete.pt', permission='news.publish')
    
    config.add_view(publish.new_item, route_name='news.publish.item.new', renderer='templates/publish/item/new.pt', permission='news.publish')
    config.add_view(publish.edit_item, route_name='news.publish.item.edit', renderer='templates/publish/item/edit.pt', permission='news.publish')
    config.add_view(publish.publish_item, route_name='news.publish.item.publish', renderer='templates/publish/item/publish.pt', permission='news.publish')
    config.add_view(publish.review_item, route_name='news.publish.item.review', renderer='templates/publish/item/review.pt', permission='news.publish')
    config.add_view(publish.delete_item, route_name='news.publish.item.delete', renderer='templates/publish/item/delete.pt', permission='news.publish')

def channel_views(config):
    from .views import channel
    
    config.add_route('news.channel.view', 'channel/view/{channel_id}')
    config.add_route('news.channel.search', 'channel/search/{channel_id}')
    config.add_route('news.channel.subscribe', 'channel/subscribe/{channel_id}')
    config.add_route('news.channel.unsubscribe', 'channel/unsubscribe/{channel_id}')
    
    config.add_view(channel.view, route_name='news.channel.view', renderer='templates/channel/view.pt', permission='news')
    config.add_view(channel.search, route_name='news.channel.search', renderer='templates/channel/search.pt', permission='news')
    
    config.add_view(channel.subscribe, route_name='news.channel.subscribe', renderer='templates/channel/subscribe.pt', permission='news')
    config.add_view(channel.unsubscribe, route_name='news.channel.unsubscribe', renderer='templates/channel/unsubscribe.pt', permission='news')

def item_views(config):
    from .views import item
    
    config.add_route('news.item.view', 'item/view/{item_id}')
    config.add_route('news.item.sign', 'item/sign/{item_id}')
    
    config.add_view(item.view, route_name='news.item.view', renderer='templates/item/view.pt', permission='news')
    config.add_view(item.sign, route_name='news.item.sign', renderer='templates/item/sign.pt', permission='news')

def general_views(config):
    from .views import general
    
    config.add_route('news.general.home', 'general/home')
    config.add_route('news.general.control_panel', 'general/control_panel')
    
    config.add_view(general.home, route_name='news.general.home', renderer='templates/general/home.pt', permission='news')
    config.add_view(general.control_panel, route_name='news.general.control_panel', renderer='templates/general/control_panel.pt', permission='news')

def documentation_views(config):
    pass
    # from ...core.documentation import basic_view
    
    # config.add_route('news.documentation.doc_page', 'documentation/doc_page')
    
    # config.add_view(basic_view("Documentation page"), route_name='news.documentation.doc_page', renderer="templates/documentation/doc_page.pt", permission="news")

def init_auth():
    from ...core.system.lib import auth
    
    ag = auth.add("news", 'Admin', {'admin', 'publish'}, rank=1)
    ag = auth.add("news", 'Publish', {'publish'}, rank=1)
    
    if site_settings_f.get_setting("news.global_visibility") == "True":
        auth.global_permissions.extend(["news"])
        site_menu['permissions'] = []

def includeme(config):
    admin_views(config)
    publish_views(config)
    channel_views(config)
    item_views(config)
    general_views(config)
    documentation_views(config)

    init_auth()
    
    # from .jobs import (
    #     empty_job
    # )
    
    # from .actions import (
    #     empty_action
    # )
    
    # from ..hooks import register_hook, append_to_hook
    # register_hook("startup", "Called when the framework starts up (after creating routes etc). Passes no arguments.")
    
    # from .lib import settings_f, render_f
    # append_to_hook("startup", settings_f.process_settings)
    # append_to_hook("startup", render_f.order_menus)
    
    # from ...core.commands import register_commands
    # from .commands import user
    
    # register_commands(user)

def install():
    """Called when the schema doesn't exist (but it's called after the schema is added)"""
    print("News install")

def update():
    """Called on install and an existing schema and when the schema doesn't exist. It is called 
    after any schema updates."""
    print("News update")


from .documentation import *
