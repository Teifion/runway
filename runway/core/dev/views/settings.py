from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...system.lib import site_settings_f
from ...base import Base, DBSession
from ...lib import common

def list_settings(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    search_text = request.params.get('search_text', '').strip()
    
    if search_text != "":
        settings = site_settings_f.get_settings_like(search_text.replace("*", "%"))
    else:
        settings = site_settings_f.get_all_settings()
    
    return dict(
        title       = "Developer: Settings",
        layout      = layout,
        pre_content = pre_content,
        settings    = settings,
    )

def module_scan(request):
    from .... import plugins
    from ...plugins.lib import find
    from ...main import _folder_path
    
    # Scan for existing module settings
    settings = site_settings_f.get_settings_like("runway.modules.%")
    for plugin_name in find.scan_for_plugins(_folder_path):
        if "runway.modules.{}".format(plugin_name) not in settings:
            site_settings_f.set_setting("runway.modules.{}".format(plugin_name), "False")
            settings["runway.modules.{}".format(plugin_name)] = "False"
    
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title         = "Developer: Settings",
        layout        = layout,
        pre_content   = pre_content,
        settings      = settings,
        reboot_needed = site_settings_f.reboot_needed(),
    )

def enable_module(request):
    module_name = request.matchdict['module_name']
    site_settings_f.set_setting(module_name, "True")
    site_settings_f.set_last_change()
    
    return HTTPFound(request.route_url('dev.settings.module_scan'))

def disable_module(request):
    module_name = request.matchdict['module_name']
    site_settings_f.set_setting(module_name, "False")
    site_settings_f.set_last_change()
    
    return HTTPFound(request.route_url('dev.settings.module_scan'))

def edit(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    message = None
    
    setting_name = request.matchdict['setting_name']
    setting_value = site_settings_f.get_setting(setting_name)
    
    if "value" in request.params:
        site_settings_f.set_setting(setting_name, request.params['value'])
        message = "success", "Setting updated, some changes may require a restart to take effect"
    
    return dict(
        title       = "Developer: Settings",
        layout      = layout,
        pre_content = pre_content,
        message     = message,
        
        setting_name  = setting_name,
        setting_value = setting_value,
    )
