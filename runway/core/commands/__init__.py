from .lib.funcs import (
    register_commands,
    execute_command,
)

def dev_views(config):
    from .views import dev
    
    config.add_route('commands.dev.list_commands', 'dev/commands/list')
    
    config.add_view(dev.list_commands, route_name='commands.dev.list_commands', renderer='templates/dev/list_commands.pt', permission='loggedin')

def includeme(config):
    dev_views(config)
