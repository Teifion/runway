site_settings = [
    ["Users", [
        ("runway.users.allow_registration", "admin", "Allow user registration", "boolean", "False", """
<ul>
    <li>When <span class="bg-success">enabled</span>, non-users are able to register on the site themselves</li>
    <li>When <span class="bg-danger">disabled</span> non-users are unable to register and can only see pages not requiring a login</li>
</ul>"""),
        ("runway.users.allow_cron", "admin", "Enable Cron jobs", "boolean", "False", """
<ul>
    <li>When <span class="bg-success">enabled</span>, users are able to use the cron job system by default</li>
    <li>When <span class="bg-danger">disabled</span> users can only make use of the cron job system when part of certain groups or when given specific permissions in the admin section</li>
</ul>
Takes effect on restart"""),
        ("runway.users.allow_widgets", "admin", "Enable Widgets", "boolean", "True", """
<ul>
    <li>When <span class="bg-success">enabled</span>, users are able to use the widget system by default</li>
    <li>When <span class="bg-danger">disabled</span> users can only make use of the widget system when part of certain groups or when given specific permissions in the admin section</li>
</ul>
Takes effect on restart"""),
        ("runway.users.allow_triggers", "admin", "Enable Triggers", "boolean", "False", """
<ul>
    <li>When <span class="bg-success">enabled</span>, users are able to use the trigger system by default</li>
    <li>When <span class="bg-danger">disabled</span> users can only make use of the trigger system when part of certain groups or when given specific permissions in the admin section</li>
</ul>
Takes effect on restart"""),
        ("runway.users.allow_groups", "admin", "Enable Groups", "boolean", "True", """
<ul>
    <li>When <span class="bg-success">enabled</span>, users are able to use the group system</li>
    <li>When <span class="bg-danger">disabled</span> users cannot edit gropus, only admins can edit/view them. However, any groups already can be searched (just not viewed from the Control Panel).</li>
</ul>
Takes effect on restart"""),
    ]],
    ["System", [
        ("runway.system.dev_email", "developer", "Developer email", "str", "", """
The email address for anything were the developer needs to be emailed."""),
        ("runway.system.admin_email", "admin", "Admin email", "str", "", """
The email address for the site owner."""),
        ("runway.system.name", "developer", "Site name", "str", "Runway", """
The name of the site. Takes effect on restart"""),
        ("runway.system.dev_message", "developer", "Developer message", "str", "", """
A developer written message to appear on the front page of the site."""),
        ("runway.system.admin_message", "admin", "Admin message", "str", "", """
An admin written message to appear on the front page of the site."""),
    ]]
]

user_settings = [
    ["System", [
        ("runway.users.primary_colour", True, "Primary colour", "colour", "", """
Your primary colour, typically used as a forground/text colour"""),
        ("runway.users.secondary_colour", True, "Secondary colour", "colour", "", """
Your secondary colour, typically used as a background colour"""),
    ]]
]

def main_views(config):
    from .views import main
    
    config.add_route('/', '/')
    config.add_route('', '')
    config.add_route('up', 'up')
    config.add_route('register', 'register')
    # config.add_route('install', 'install')
    
    config.add_view(main.root, route_name='/', renderer='templates/main/home.pt', permission='loggedin')
    config.add_view(main.root, route_name='', renderer='templates/main/home.pt', permission='loggedin')
    config.add_view(main.up, route_name='up', renderer='string')
    config.add_view(main.register, route_name='register', renderer='templates/main/register.pt', permission='view')

def authentication_views(config):    
    from .views import authentication
    
    config.add_route('core.login', 'login')
    config.add_route('core.logout', 'logout')
    config.add_route('core.external_auth', 'external_auth')
    
    # Now link the views
    config.add_view(authentication.login, route_name='core.login', renderer='templates/authentication/login.pt', permission='view')
    config.add_view(authentication.logout, route_name='core.logout', permission='view')
    config.add_view(authentication.external_auth, route_name='core.external_auth', renderer='templates/authentication/external_auth.pt', permission='loggedin')
    
    config.add_forbidden_view(authentication.forbidden, renderer='templates/authentication/forbidden.pt')

def user_views(config):
    from .views import user
    config.add_route('user.control_panel', 'user/control_panel')
    config.add_route('user.account', 'user/account')
    
    config.add_route('user.groups.list', 'user/groups/list')
    config.add_route('user.groups.create', 'user/groups/create')
    config.add_route('user.groups.remove', 'user/groups/remove')
    config.add_route('user.groups.view', 'user/groups/view/{group_id}')
    config.add_route('user.groups.edit', 'user/groups/edit/{group_id}')
    config.add_route('user.groups.add_member', 'user/groups/add_member/{group_id}')
    config.add_route('user.groups.remove_member', 'user/groups/remove_member/{group_id}')
    
    config.add_view(user.control_panel, route_name='user.control_panel', renderer='templates/user/control_panel.pt', permission='loggedin')
    config.add_view(user.account, route_name='user.account', renderer='templates/user/account.pt', permission='loggedin')
    
    config.add_view(user.list_groups, route_name='user.groups.list', renderer='templates/user/groups/list.pt', permission='loggedin')
    config.add_view(user.create_group, route_name='user.groups.create', renderer='templates/user/groups/create.pt', permission='loggedin')
    config.add_view(user.remove_group, route_name='user.groups.remove', renderer='templates/user/groups/remove.pt', permission='loggedin')
    config.add_view(user.view_group, route_name='user.groups.view', renderer='templates/user/groups/view.pt', permission='loggedin')
    config.add_view(user.edit_group, route_name='user.groups.edit', renderer='templates/user/groups/edit.pt', permission='loggedin')
    config.add_view(user.add_member_to_group, route_name='user.groups.add_member', permission='loggedin')
    config.add_view(user.remove_member_from_group, route_name='user.groups.remove_member', permission='loggedin')
    
def ajax_views(config):
    from .views import ajax
    config.add_route('ajax.user.search', 'ajax/user/search')
    config.add_route('ajax.group.search', 'ajax/group/search')
    
    config.add_view(ajax.user_search, route_name='ajax.user.search', renderer="string")
    config.add_view(ajax.group_search, route_name='ajax.group.search', renderer="string")
    
def documentation_views(config):
    from ..documentation import basic_view
    from . import documentation
    
    config.add_route('user.groups.documentation.edit_group', 'user/groups/documentation/edit_group')
    config.add_route('user.documentation.settings', 'user/documentation/settings')
    
    config.add_view(
        basic_view(documentation.EditGroup),
        route_name='user.groups.documentation.edit_group',
        renderer="templates/documentation/user/groups/edit_group.pt",
        permission="loggedin"
    )
    
    config.add_view(
        basic_view(documentation.UserSettings),
        route_name='user.documentation.settings',
        renderer="templates/documentation/user/settings.pt",
        permission="loggedin"
    )
    
    config.add_route('system.widgets.documentation.user_picker', 'system/widgets/documentation/user_picker')
    config.add_route('system.widgets.documentation.group_picker', 'system/widgets/documentation/group_picker')
    config.add_route('system.widgets.documentation.combo_picker', 'system/widgets/documentation/combo_picker')
    
    config.add_view(
        basic_view(documentation.UserPickerWidget),
        route_name='system.widgets.documentation.user_picker',
        renderer="templates/documentation/widgets/user_picker.pt",
        permission="developer"
    )
    config.add_view(
        basic_view(documentation.GroupPickerWidget),
        route_name='system.widgets.documentation.group_picker',
        renderer="templates/documentation/widgets/group_picker.pt",
        permission="developer"
    )
    config.add_view(
        basic_view(documentation.ComboPickerWidget),
        route_name='system.widgets.documentation.combo_picker',
        renderer="templates/documentation/widgets/combo_picker.pt",
        permission="developer"
    )

def exception_views(config):
    from .views import exceptions
    from ..lib.common import GracefulException
    from sqlalchemy.exc import DBAPIError
    
    from pyramid.exceptions import (
        NotFound
    )
    
    config.add_route('exceptions.deactivated_user', 'exceptions/deactivated_user')
    
    config.add_view(exceptions.deactivated_user, route_name='exceptions.deactivated_user', renderer="templates/exceptions/deactivated_user.pt")
    
    config.add_view(exceptions.display_graceful_exception, context=GracefulException, renderer='templates/exceptions/fail_gracefully.pt')
    config.add_view(exceptions.general_exception, context=Exception, renderer='templates/exceptions/general_exception.pt')
    config.add_view(exceptions.dbapi_error, context=DBAPIError, renderer='templates/exceptions/dbapi_error.pt')
    config.add_view(exceptions.not_found_exception, context=NotFound, renderer='templates/exceptions/404.pt')

def api_init():
    from ..apis.lib.api_f import register_handler
    from .apis import user_handlers
    
    register_handler("users", user_handlers.users, "admin")
    register_handler("groups", user_handlers.groups, "admin")

def includeme(config):
    authentication_views(config)
    main_views(config)
    user_views(config)
    exception_views(config)
    ajax_views(config)
    documentation_views(config)
    
    api_init()
    
    from .jobs import (
        prune_logs,
        backup,
    )
    
    from .actions import (
        formatter,
        email,
        get_user,
    )
    
    from ..hooks import register_hook, append_to_hook
    register_hook("startup", "Called when the framework starts up (after creating routes etc). Passes no arguments.")
    register_hook("post_startup", "Called after startup.")
    register_hook("pre_render", "Called after startup. Passes the request object.")
    
    from .lib import site_settings_f, user_settings_f, render_f
    append_to_hook("startup", site_settings_f.process_settings)
    append_to_hook("startup", user_settings_f.process_settings)
    append_to_hook("post_startup", render_f.order_menus)
    
    
    append_to_hook("pre_render", lambda request: print("\n\n{}\n\n".format(request.path)))
    
    # Commands
    from ...core.commands import register_commands
    from .commands import settings
    
    register_commands(settings)

def install():
    from .lib import install_f
    install_f.system_install()

from .documentation import *