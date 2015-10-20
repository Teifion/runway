def entry_point_views(config):
    from .views import entry_points
    
    config.add_route('api.request', 'request')
    config.add_view(entry_points.api_request, route_name='api.request', renderer='string')

def admin_views(config):
    from .views import admin
    
    config.add_route('api.admin.home', 'admin/home')
    config.add_route('api.admin.grant', 'admin/grant')
    config.add_route('api.admin.revoke', 'admin/revoke/{key_id}')
    
    config.add_view(admin.home, route_name='api.admin.home', renderer='templates/admin/home.pt', permission='developer')
    config.add_view(admin.grant, route_name='api.admin.grant', permission='developer')
    config.add_view(admin.revoke, route_name='api.admin.revoke', permission='developer')

def includeme(config):
    admin_views(config)
    entry_point_views(config)
