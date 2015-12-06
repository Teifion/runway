from .lib.funcs import (
    register_hook,
    append_to_hook,
    call_hook,
)

def dev_views(config):
    from .views import dev
    
    config.add_route('hooks.dev.list_hooks', 'dev/hooks/list')
    
    config.add_view(dev.list_hooks, route_name='hooks.dev.list_hooks', renderer='templates/dev/list_hooks.pt', permission='loggedin')

def documentation_views(config):
    from ..documentation import basic_view
    from . import documentation
    
    # config.add_route('hooks.documentation.user', 'admin/documentation/user')
    # config.add_route('admin.documentation.adding_users', 'admin/documentation/adding_users')
    
    # config.add_view(
    #     basic_view(documentation.UserAdministration),
    #     route_name='admin.documentation.user',
    #     renderer="templates/documentation/user.pt",
    #     permission="admin"
    # )

def includeme(config):
    dev_views(config)
    documentation_views(config)

from .documentation import *