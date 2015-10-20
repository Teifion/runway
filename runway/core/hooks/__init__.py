from .lib.funcs import (
    register_hook,
    append_to_hook,
    call_hook,
)

def dev_views(config):
    from .views import dev
    
    config.add_route('hooks.dev.list_hooks', 'dev/hooks/list')
    
    config.add_view(dev.list_hooks, route_name='hooks.dev.list_hooks', renderer='templates/dev/list_hooks.pt', permission='loggedin')

def includeme(config):
    dev_views(config)
