route_prefix = "empty_module"

# site_settings = [
#     ["Empty module", [
#         ("empty_module.setting", "su", "Label", "Type", "Default", """Description"""),
#     ]],
# ]

def admin_views(config):
    from .views import admin
    
    config.add_route('empty_module.admin.home', 'admin/home')
    
    config.add_view(admin.home, route_name='empty_module.admin.home', renderer='templates/admin/home.pt', permission='empty_module.admin')

def documentation_views(config):
    from .views import documentation
    config.add_route('user.groups.documentation.edit_group', 'user/groups/documentation/edit_group')
    
    config.add_view(documentation.basic, route_name='user.groups.documentation.edit_group', renderer="templates/documentation/user/groups/edit_group.pt", permission="loggedin")

def init_auth():
    from ..system.lib import auth
    
    ag = auth.add("empty_module", 'Admin', {'admin'}, rank=1)

def includeme(config):
    pass

from .documentation import *