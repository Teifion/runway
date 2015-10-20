def general_views(config):
    from .views import general
    config.add_route('plugins.home', 'home')
    config.add_view(general.home, route_name='plugins.home', renderer='templates/general/home.pt', permission='admin')

def includeme(config):
    general_views(config)
