route_prefix = "news"

from . import schema

site_menu = {
    "id": "news",
    "permissions": [],
    "route":"news.general.home",
    "icon": "fa-newspaper-o",
    "text": "News",
    "order": 20,
}

site_settings = [
    # ["News", [
    #     ("news.setting", "Permissions", "Label", "Type", "Default", """Description"""),
    # ]],
]

user_settings = [
    # ["News", [
    #     ("news.setting", True, "Label", "Type", "Default", """Description"""),
    # ]],
]

admin_menu = (
    ("news.general.home", "fa-newspaper-o", "News", "news.admin"),
)

def admin_views(config):
    from .views import admin
    
    config.add_route('news.admin.home', 'admin/home')
    
    config.add_route('news.admin.channel.new', 'admin/channel/new')
    config.add_route('news.admin.channel.edit', 'admin/channel/edit')
    config.add_route('news.admin.channel.delete', 'admin/channel/delete')
    
    config.add_view(admin.home, route_name='news.admin.home', renderer='templates/admin/home.pt', permission='news.admin')
    
    
    config.add_view(admin.new_channel, route_name='news.admin.channel.new', renderer='templates/admin/channel/new.pt', permission='news.admin')
    config.add_view(admin.edit_channel, route_name='news.admin.channel.edit', renderer='templates/admin/channel/edit.pt', permission='news.admin')
    config.add_view(admin.delete_channel, route_name='news.admin.channel.delete', renderer='templates/admin/channel/delete.pt', permission='news.admin')

def publish_views(config):
    from .views import publish
    
    config.add_route('news.publish.home', 'publish/home')
    
    config.add_view(publish.home, route_name='news.publish.home', renderer='templates/publish/home.pt', permission='news.publish')

def general_views(config):
    from .views import general
    
    config.add_route('news.general.home', 'general/home')
    config.add_route('news.general.control_panel', 'general/control_panel')
    
    config.add_view(general.home, route_name='news.general.home', renderer='templates/general/home.pt', permission='loggedin')
    config.add_view(general.control_panel, route_name='news.general.control_panel', renderer='templates/general/control_panel.pt', permission='loggedin')

def documentation_views(config):
    pass
    # from ...core.documentation import basic_view
    
    # config.add_route('news.documentation.doc_page', 'documentation/doc_page')
    
    # config.add_view(basic_view("Documentation page"), route_name='news.documentation.doc_page', renderer="templates/documentation/doc_page.pt", permission="loggedin")

def init_auth():
    from ...core.system.lib import auth
    
    ag = auth.add("news", 'Admin', {'admin', 'publish'}, rank=1)
    ag = auth.add("news", 'Publish', {'publish'}, rank=1)

def includeme(config):
    admin_views(config)
    publish_views(config)
    documentation_views(config)
    general_views(config)
    
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
