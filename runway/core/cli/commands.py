from ..system.lib import settings_f

def activate_module(options):
    results = []
    
    for module_name in options.vals:
        settings_f.set_setting("runway.modules.{}".format(module_name), "True")
        settings_f.set_last_change()
        
        results.append("Activated {}".format(module_name))
    
    return "\n".join(results)

def deactivate_module(options):
    results = []
    
    for module_name in options.vals:
        settings_f.set_setting("runway.modules.{}".format(module_name), "False")
        settings_f.set_last_change()
        
        results.append("Activated {}".format(module_name))
    
    return "\n".join(results)
