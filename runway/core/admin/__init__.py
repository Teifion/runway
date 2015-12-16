admin_menu = (
    ("admin.settings", "fa-gears", "Settings", "su"),
    ("themes.admin.home", "fa-paste", "Themes", "su"),
    ("admin.usage.home", "fa-line-chart", "Usage reports", "admin.usage"),
    ("admin.groups.list", "fa-group", "User groups", ""),
    ("cron.admin.home", "fa-clock-o", "Cron jobs", "cron.admin"),
)

def general_views(config):
    from .views import general
    
    config.add_route('admin.home', 'home')
    config.add_route('admin.settings', 'settings')
    config.add_route('admin.site_stats', 'site_stats')
    config.add_route('admin.schedule_restart', 'schedule_restart')
    
    config.add_view(general.home, route_name='admin.home', renderer='templates/general/home.pt', permission='admin')
    config.add_view(general.settings, route_name='admin.settings', renderer='templates/general/settings.pt', permission='su')
    config.add_view(general.site_stats, route_name='admin.site_stats', renderer='templates/general/site_stats.pt', permission='admin.usage')
    config.add_view(general.schedule_restart, route_name='admin.schedule_restart', renderer='templates/general/schedule_restart.pt', permission='admin.su')

def group_views(config):
    from .views import groups
    
    config.add_route('admin.groups.edit', 'groups/edit/{group_id}')
    config.add_route('admin.groups.view', 'groups/view/{group_id}')
    config.add_route('admin.groups.create', 'groups/create')
    config.add_route('admin.groups.list', 'groups/list')
    config.add_route('admin.groups.search', 'groups/search')
    
    config.add_route('admin.groups.remove', 'groups/remove')
    config.add_route('admin.groups.add_member', 'groups/add_member/{group_id}')
    config.add_route('admin.groups.remove_member', 'groups/remove_member/{group_id}')
    
    config.add_view(groups.edit, route_name='admin.groups.edit', renderer='templates/groups/edit.pt', permission='admin.user.create')
    config.add_view(groups.view, route_name='admin.groups.view', renderer='templates/groups/view.pt', permission='admin.user.view')
    config.add_view(groups.create, route_name='admin.groups.create', renderer='templates/groups/create.pt', permission='admin.user.create')
    config.add_view(groups.list_groups, route_name='admin.groups.list', renderer='templates/groups/list.pt', permission='admin.user.view')
    config.add_view(groups.search, route_name='admin.groups.search', renderer='templates/groups/list.pt', permission='admin.user.view')
    config.add_view(groups.remove, route_name='admin.groups.remove', renderer='templates/groups/remove.pt', permission='admin.user.create')
    
    config.add_view(groups.add_member, route_name='admin.groups.add_member', permission='admin.user.create')
    config.add_view(groups.remove_member, route_name='admin.groups.remove_member', permission='admin.user.create')

def user_views(config):
    from .views import user
    
    config.add_route('admin.user.search_username', 'user/search_username')
    config.add_route('admin.user.search_display_name', 'user/search_display_name')
    config.add_route('admin.user.search_group', 'user/search_group')
    config.add_route('admin.user.search_permission', 'user/search_permission')
    
    config.add_route('admin.user.list', 'user/list')
    
    config.add_route('admin.user.edit', 'user/edit/{user_id}')
    config.add_route('admin.user.view', 'user/view/{user_id}')
    config.add_route('admin.user.export', 'user/export')
    
    config.add_route('admin.user.activate', 'user/activate/{user_id}')
    config.add_route('admin.user.deactivate', 'user/deactivate/{user_id}')
    
    config.add_route('admin.user.add_permission_group_membership', 'user/add_permission_group_membership')
    config.add_route('admin.user.remove_permission_group_membership', 'user/remove_permission_group_membership')
    
    config.add_route('admin.user.add_relationship', 'user/add_relationship')
    config.add_route('admin.user.remove_relationship', 'user/remove_relationship')
    
    config.add_route('admin.user.add_security_check', 'user/add_security_check')
    config.add_route('admin.user.remove_security_check', 'user/remove_security_check')
    
    config.add_route('admin.user.mass_add', 'user/mass_add')
    config.add_route('admin.user.quick_add', 'user/quick_add')
    
    config.add_route('admin.user.list_relationship_types', 'user/list_relationship_types')
    config.add_route('admin.user.add_relationship_type', 'user/add_relationship_type')
    config.add_route('admin.user.edit_relationship_type', 'user/edit_relationship_type/{type_id}')
    config.add_route('admin.user.remove_relationship_type', 'user/remove_relationship_type/{type_id}')
    
    config.add_view(user.search_username, route_name='admin.user.search_username', renderer='templates/user/search_username.pt', permission='admin.user.search')
    config.add_view(user.search_display_name, route_name='admin.user.search_display_name', renderer='templates/user/search_display_name.pt', permission='admin.user.search')
    config.add_view(user.search_group, route_name='admin.user.search_group', renderer='templates/user/search_group.pt', permission='admin.user.search')
    config.add_view(user.search_permission, route_name='admin.user.search_permission', renderer='templates/user/search_permission.pt', permission='admin.user.search')
    
    config.add_view(user.list_users, route_name='admin.user.list', renderer='templates/user/list.pt', permission='admin.user.search')
    
    config.add_view(user.edit, route_name='admin.user.edit', renderer='templates/user/edit.pt', permission='admin.user.edit')
    config.add_view(user.view, route_name='admin.user.view', renderer='templates/user/view.pt', permission='admin.user.view')
    
    config.add_view(user.activate, route_name='admin.user.activate', permission='admin.user.edit')
    config.add_view(user.deactivate, route_name='admin.user.deactivate', permission='admin.user.edit')
    
    config.add_view(user.export, route_name='admin.user.export', renderer='string', permission='admin.usage')
    
    config.add_view(user.add_permission_group_membership, route_name='admin.user.add_permission_group_membership', permission='admin.user.edit')
    config.add_view(user.remove_permission_group_membership, route_name='admin.user.remove_permission_group_membership', permission='admin.user.edit')
    
    config.add_view(user.add_security_check, route_name='admin.user.add_security_check', permission='admin.user.edit')
    config.add_view(user.remove_security_check, route_name='admin.user.remove_security_check', permission='admin.user.edit')
    
    config.add_view(user.add_relationship, route_name='admin.user.add_relationship', permission='admin.user.edit')
    config.add_view(user.remove_relationship, route_name='admin.user.remove_relationship', permission='admin.user.edit')
    
    config.add_view(user.mass_add, route_name='admin.user.mass_add', renderer='templates/user/mass_add.pt', permission='admin.user.create')
    config.add_view(user.quick_add, route_name='admin.user.quick_add', renderer='templates/user/quick_add.pt', permission='admin.user.create')
    
    config.add_view(user.list_relationship_types, route_name='admin.user.list_relationship_types', renderer='templates/user/list_relationship_types.pt', permission='admin.su')
    config.add_view(user.add_relationship_type, route_name='admin.user.add_relationship_type', permission='admin.su')
    config.add_view(user.edit_relationship_type, route_name='admin.user.edit_relationship_type', renderer='templates/user/edit_relationship_type.pt', permission='admin.su')
    config.add_view(user.remove_relationship_type, route_name='admin.user.remove_relationship_type', permission='admin.su')

def usage_views(config):
    from .views import usage
    
    config.add_route('admin.usage.home', 'usage/home')
    config.add_route('admin.usage.user.search', 'usage/user/search')
    config.add_route('admin.usage.user.history', 'usage/user/history/{user_id}')
    config.add_route('admin.usage.user.overview', 'usage/user/overview/{user_id}')
    
    config.add_route('admin.usage.group.search', 'usage/group/search')
    config.add_route('admin.usage.group.history', 'usage/group/history/{group_id}')
    config.add_route('admin.usage.group.overview', 'usage/group/overview/{group_id}')
    
    config.add_route('admin.usage.aggregate', 'usage/aggregate')
    
    config.add_route('admin.usage.latest', 'usage/latest')
    
    config.add_view(usage.home, route_name='admin.usage.home', renderer='templates/usage/home.pt', permission='admin.usage')
    
    config.add_view(usage.user_search, route_name='admin.usage.user.search', renderer='templates/usage/user_search.pt', permission='admin.usage')
    config.add_view(usage.user_history, route_name='admin.usage.user.history', renderer='templates/usage/user_history.pt', permission='admin.usage')
    config.add_view(usage.user_overview, route_name='admin.usage.user.overview', renderer='templates/usage/user_overview.pt', permission='admin.usage')
    
    config.add_view(usage.group_search, route_name='admin.usage.group.search', renderer='templates/usage/group_search.pt', permission='admin.usage')
    config.add_view(usage.group_history, route_name='admin.usage.group.history', renderer='templates/usage/group_history.pt', permission='admin.usage')
    config.add_view(usage.group_overview, route_name='admin.usage.group.overview', renderer='templates/usage/group_overview.pt', permission='admin.usage')
    
    config.add_view(usage.aggregate, route_name='admin.usage.aggregate', renderer='templates/usage/aggregate.pt', permission='admin.usage')
    
    config.add_view(usage.latest, route_name='admin.usage.latest', renderer='templates/usage/latest.pt', permission='admin.usage')

def audit_views(config):
    from .views import audit
    
    config.add_route('admin.audit.list_logs', 'audit/list_logs')
    
    config.add_view(audit.list_logs, route_name='admin.audit.list_logs', renderer='templates/audit/list_logs.pt', permission='admin.usage')

def documentation_views(config):
    from ..documentation import basic_view
    from . import documentation
    
    config.add_route('admin.documentation.user', 'admin/documentation/user')
    config.add_route('admin.documentation.adding_users', 'admin/documentation/adding_users')
    config.add_route('admin.documentation.settings', 'admin/documentation/settings')
    
    config.add_view(
        basic_view(documentation.UserAdministration),
        route_name='admin.documentation.user',
        renderer="templates/documentation/user.pt",
        permission="admin"
    )
    config.add_view(
        basic_view(documentation.AddingUsers),
        route_name='admin.documentation.adding_users',
        renderer="templates/documentation/adding_users.pt",
        permission="admin"
    )
    config.add_view(
        basic_view(documentation.Settings),
        route_name='admin.documentation.settings',
        renderer="templates/documentation/settings.pt",
        permission="admin"
    )
    

def init_auth():
    from ..system.lib import auth
    
    ag = auth.add("admin", 'Moderator',                 {'moderator', 'user.view', 'user.search', 'aggregate_usage'}, rank=1, admin_rank=1)
    ag = auth.add("admin", 'Administrator',        ag | {'user.edit', 'user.create'}, rank=2, admin_rank=2)
    ag = auth.add("admin", 'Senior administrator', ag | {'usage'}, rank=3, admin_rank=3)
    ag = auth.add("admin", 'Superuser',            ag | {'su'}, rank=3, admin_rank=4)
    
    # Set developer to admin_rank of 10
    auth.RootFactory.__acl__[0].kwargs['admin_rank'] = 10
    
    # Super user to 9
    auth.RootFactory.__acl__[1].kwargs['admin_rank'] = 9

def includeme(config):
    general_views(config)
    user_views(config)
    group_views(config)
    usage_views(config)
    audit_views(config)
    documentation_views(config)
    init_auth()
    
    from ...core.commands import register_commands
    from ...core.hooks import register_hook, append_to_hook
    from .commands import user
    
    register_commands(user)
    
    from .jobs import (
        restart,
    )
    
    register_hook("admin.sections", "Each function call should return a (url, icon, label, permissions) tuple which will be used to populate lists within the admin section.")

from .documentation import *
