route_prefix = "themes"

site_settings = [
    ["Themes", [
        ("runway.themes.site_theme", "admin.su", "Site theme", "str", "sb_admin_v2", """Theme used by the site"""),
    ]],
]

def admin_views(config):
    from .views import admin
    
    config.add_route('themes.admin.home', 'admin/home')
    config.add_route('themes.admin.select_theme', 'admin/select_theme/{theme_name}')
    config.add_route('themes.admin.view_theme', 'admin/view_theme/{theme_name}')
    
    config.add_view(admin.home, route_name='themes.admin.home', renderer='templates/admin/home.pt', permission='su')
    config.add_view(admin.select_theme, route_name='themes.admin.select_theme', renderer='templates/admin/select_theme.pt', permission='su')
    config.add_view(admin.view_theme, route_name='themes.admin.view_theme', renderer='templates/admin/view_theme.pt', permission='su')

def init_auth():
    from ..system.lib import auth

def includeme(config):
    admin_views(config)
    init_auth()
    
    from .lib import themes_f
    from ..hooks import append_to_hook
    
    from ...core.commands import register_commands
    from .commands import themes
    
    register_commands(themes)
    
    append_to_hook("startup", themes_f._startup)
    
    
