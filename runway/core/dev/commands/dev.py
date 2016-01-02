from ....core.commands.lib import funcs
from .... import plugins
from ...plugins.lib import find
from ...main import _folder_path
from ....core.system.lib import user_f
import transaction
from ....core.base import DBSession
from ....core.system.models import Setting
from ....core.system.models.user import (
    User,
)

from ...system.lib import site_settings_f
from ....core.system.lib import backup_f

def list_modules():
    """
    () -> String
    Outputs a list of all available modules and their current state.
    """
    modules = []
    
    # Scan for existing module settings
    settings = site_settings_f.get_settings_like("runway.modules.%")
    for plugin_name in find.scan_for_plugins(_folder_path):
        active = settings.get("runway.modules.{}".format(plugin_name), "False")
        # if "runway.modules.{}".format(plugin_name) not in settings:
        #     site_settings_f.set_setting("runway.modules.{}".format(plugin_name), "False")
        #     settings["runway.modules.{}".format(plugin_name)] = "False"
        
        if active == "True":
            active = "[g]Active[/g]"
        else:
            active = "[r]Deactivated[/r]"
        
        modules.append("{:20} {}".format(plugin_name, active))
    
    return "\n".join(modules)

def activate_all_modules():
    """
    () -> IO String
    Activates all modules it can find in the plugins folder
    """
    
    query = """UPDATE {}
        SET value = 'True'
        WHERE "name" LIKE 'runway.modules.%'
        """.format(Setting.__tablename__)
    
    with transaction.manager:
        DBSession.execute(query)
        DBSession.execute("COMMIT")
    
    return "Activated everything"

def activate_module(*names):
    """
    [String] -> IO String
    Takes a list of module names and sets them to active. If already active it will not throw an error.
    """
    names = list(names)
    
    with transaction.manager:
        for module_name in names:
            site_settings_f.set_setting("runway.modules.{}".format(module_name), "True")
            site_settings_f.set_last_change()
    
    return "Activated: {}".format(", ".join(names))

def deactivate_module(*names):
    """
    [String] -> IO String
    Takes a list of module names and deactivates them. If already deactivated it will not throw an error.
    """
    names = list(names)
    
    with transaction.manager:
        for module_name in names:
            site_settings_f.set_setting("runway.modules.{}".format(module_name), "False")
            site_settings_f.set_last_change()
    
    return "Activated: {}".format(", ".join(names))

def commands():
    """
    () -> String
    List commands available.
    """
    
    command_list = list(funcs._command_dict.keys())
    command_list.sort()
    
    for c in command_list:
        the_func = funcs._command_dict[c]
        
        doc = the_func.__doc__.strip() if the_func.__doc__ != None else ""
        # doc = doc.replace("\n    ", "    ")
        
        if doc != "":
            if "\n" in doc:
                print("  {}: {}\n".format(the_func.__name__, doc))
            else:
                print("  {}: {}".format(the_func.__name__, doc))
        else:
            print("  {}".format(the_func.__name__))
    
    # print("\n\n")
    # print(dir(the_func))
    # print(the_func.__module__)

def install():
    """
    () -> IO ()
    Generates modele-defined tables and updates the schema.
    """
    from ....core.main import install as main_install
    main_install()
    
    
def encode13(the_string):
    """
    String -> String
    """
    import codecs
    return codecs.encode(the_string, "rot_13")

def decode13(the_string):
    """
    String -> String
    """
    import codecs
    return codecs.decode(the_string, "rot_13")
