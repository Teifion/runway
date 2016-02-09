def debugging_views(config):
    from .views import debugging
    
    config.add_route('dev.debugging.slow_pages', 'debugging/slow_pages')
    config.add_route('dev.debugging.slow_drilldown', 'debugging/slow_drilldown')
    config.add_route('dev.debugging.neighbouring_logs', 'debugging/neighbouring_logs')
    config.add_route('dev.debugging.test_page', 'debugging/test_page')
    config.add_route('dev.debugging.permissions', 'debugging/permissions')
    
    config.add_view(debugging.slow_pages, route_name='dev.debugging.slow_pages', renderer='templates/debugging/slow_pages.pt', permission='developer')
    config.add_view(debugging.slow_drilldown, route_name='dev.debugging.slow_drilldown', renderer='templates/debugging/slow_drilldown.pt', permission='developer')
    config.add_view(debugging.neighbouring_logs, route_name='dev.debugging.neighbouring_logs', renderer='templates/debugging/neighbouring_logs.pt', permission='developer')
    config.add_view(debugging.test_page, route_name='dev.debugging.test_page', renderer='templates/debugging/test_page.pt', permission='developer')
    config.add_view(debugging.permissions, route_name='dev.debugging.permissions', renderer='templates/debugging/permissions.pt', permission='developer')

def exception_views(config):
    from .views import exceptions
    
    config.add_route('dev.exception.edit', 'exception/edit/{exception_id}')
    config.add_route('dev.exception.list', 'exception/list')
    # config.add_route('dev.exception.trim', 'exception/trim/{exception_id}')
    config.add_route('dev.exception.hide', 'exception/hide/{exception_id}')
    config.add_route('dev.exception.hide_all', 'exception/hide_all')
    
    config.add_view(exceptions.edit, route_name='dev.exception.edit', renderer='templates/exceptions/edit.pt', permission='developer')
    config.add_view(exceptions.list_exceptions, route_name='dev.exception.list', renderer='templates/exceptions/list.pt', permission='errors')
    # config.add_view(exceptions.trim, route_name='dev.exception.trim', permission='developer')
    config.add_view(exceptions.hide, route_name='dev.exception.hide', permission='errors')
    config.add_view(exceptions.hide_all, route_name='dev.exception.hide_all', permission='errors')

def general_views(config):
    from .views import general
    
    config.add_route('dev.home', 'home')
    # config.add_route('dev.restart', 'restart')
    config.add_route('dev.generate_exception', 'generate_exception')
    config.add_route('dev.installer', 'installer')
    config.add_route('dev.schemas', 'schemas')
    config.add_route('dev.get_backup', 'get_backup')
    
    config.add_view(general.home, route_name='dev.home', renderer='templates/general/home.pt', permission='developer')
    # config.add_view(general.restart, route_name='dev.restart', renderer='templates/general/restart.pt', permission='developer')
    config.add_view(general.generate_exception, route_name='dev.generate_exception', permission='errors')
    config.add_view(general.installer, route_name='dev.installer', renderer='templates/general/installer.pt', permission='developer')
    config.add_view(general.schemas, route_name='dev.schemas', renderer='templates/general/schemas.pt', permission='developer')
    config.add_view(general.get_backup, route_name='dev.get_backup', renderer='string', permission='backup')

def settings_views(config):
    from .views import settings
    
    config.add_route('dev.settings.list', 'settings/list')
    config.add_route('dev.settings.edit', 'settings/edit/{setting_name}')
    config.add_route('dev.settings.module_scan', 'settings/module_scan')
    config.add_route('dev.settings.enable_module', 'settings/enable_module/{module_name}')
    config.add_route('dev.settings.disable_module', 'settings/disable_module/{module_name}')
    
    config.add_view(settings.list_settings, route_name='dev.settings.list', renderer='templates/settings/list.pt', permission='developer')
    config.add_view(settings.edit, route_name='dev.settings.edit', renderer='templates/settings/edit.pt', permission='developer')
    
    config.add_view(settings.module_scan, route_name='dev.settings.module_scan', renderer='templates/settings/module_scan.pt', permission='developer')
    config.add_view(settings.enable_module, route_name='dev.settings.enable_module', permission='developer')
    config.add_view(settings.disable_module, route_name='dev.settings.disable_module', permission='developer')

def documentation_views(config):
    from ..documentation import basic_view
    from . import documentation
    
    config.add_route('dev.documentation.home', 'documentation/home')
    config.add_route('dev.documentation.widgets', 'documentation/widgets')
    config.add_route('dev.documentation.testing', 'documentation/testing')
    # config.add_route('dev.documentation.form_validation', 'documentation/form_validation')
    config.add_route('dev.documentation.demo_mode', 'documentation/demo_mode')
    config.add_route('dev.documentation.new_module', 'documentation/new_module')
    config.add_route('dev.documentation.schemas', 'documentation/schemas')
    
    config.add_view(
        basic_view(documentation.Widgets),
        route_name='dev.documentation.widgets',
        renderer="templates/documentation/widgets.pt",
        permission="developer"
    )
    
    # config.add_view(
    #     basic_view(documentation.Testing),
    #     route_name='dev.documentation.testing',
    #     renderer="templates/documentation/testing.pt",
    #     permission="developer"
    # )
    
    # config.add_view(
    #     basic_view(documentation.FormValidation),
    #     route_name='dev.documentation.form_validation',
    #     renderer="templates/documentation/form_validation.pt",
    #     permission="developer"
    # )
    
    # config.add_view(
    #     basic_view(documentation.DemoMode),
    #     route_name='dev.documentation.demo_mode',
    #     renderer="templates/documentation/demo_mode.pt",
    #     permission="developer"
    # )
    
    config.add_view(
        basic_view(documentation.DevHome),
        route_name='dev.documentation.home',
        renderer="templates/documentation/home.pt",
        permission="developer"
    )
    
    config.add_view(
        basic_view(documentation.NewModule),
        route_name='dev.documentation.new_module',
        renderer="templates/documentation/new_module.pt",
        permission="developer"
    )
    
    config.add_view(
        basic_view(documentation.Schemas),
        route_name='dev.documentation.schemas',
        renderer="templates/documentation/schemas.pt",
        permission="developer"
    )

def includeme(config):
    general_views(config)
    exception_views(config)
    settings_views(config)
    debugging_views(config)
    documentation_views(config)
    
    from .widgets import (
        errors_widget,
        load_widget,
    )
    
    from .triggers import (
        error,
    )
    
    from ...core.commands import register_commands
    from .commands import dev
    
    register_commands(dev)
    
    from .apis import (
        dev_apis,
    )

from .documentation import *
