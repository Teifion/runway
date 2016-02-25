def entry_point_views(config):
    from .views import entry_points
    
    config.add_route('api.request', 'request')
    config.add_view(entry_points.api_request, route_name='api.request', renderer='string')

def admin_views(config):
    from .views import admin
    
    config.add_route('api.admin.home', 'admin/home')
    config.add_route('api.admin.grant', 'admin/grant')
    config.add_route('api.admin.revoke', 'admin/revoke/{key_id}')
    config.add_route('api.admin.view', 'admin/view/{api_name}')
    
    config.add_view(admin.home, route_name='api.admin.home', renderer='templates/admin/home.pt', permission='developer')
    config.add_view(admin.view, route_name='api.admin.view', renderer='templates/admin/view.pt', permission='developer')
    config.add_view(admin.grant, route_name='api.admin.grant', permission='developer')
    config.add_view(admin.revoke, route_name='api.admin.revoke', permission='developer')

def documentation_views(config):
    from . import documentation
    from ...core.documentation import basic_view
    
    config.add_route('api.documentation.add_handler', 'documentation/add_handler')
    
    config.add_view(
        basic_view(documentation.AddAPIHandler),
        route_name='api.documentation.add_handler',
        renderer="templates/documentation/add_handler.pt",
        permission="developer"
    )

def includeme(config):
    admin_views(config)
    entry_point_views(config)
    documentation_views(config)
    
    from .lib import api_f
    from ..hooks import append_to_hook
    
    append_to_hook("startup", api_f.collect_handlers)
    
    from .apis import (
        dummy,
    )

from .models import APIHandler
from .documentation import *
