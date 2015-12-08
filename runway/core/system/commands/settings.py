from ....core.commands.lib import funcs
from ....core.system.lib import site_settings_f
import transaction
from ...base import DBSession
from ...system.models.user import (
    User,
)

def view_setting(setting_name):
    """
    String -> IO String
    Takes a setting name and prints the value
    """
    
    setting_name = "%{}%".format(setting_name)
    
    setting_list = site_settings_f.get_settings_like(setting_name)
    
    results = ["Found {} setting{}".format(
        len(setting_list),
        "s" if len(setting_list) != 1 else "",
    )]
    
    max_name_size = max(map(len, setting_list.keys()))
    max_value_size = max(map(len, setting_list.values()))
    format_string = "{:%s} {:%s}" % (max_name_size + 3, max_value_size)
    
    
    if len(setting_list) > 0:
        results.append(format_string.format("Name", "Value"))
        results.append("=" * (max_name_size + max_value_size + 4))
    
    for name, value in setting_list.items():
        results.append(format_string.format(name, value))
    
    return "\n".join(results)

  
def add_setting(setting_name, new_value):
    """
    String -> IO String
    Takes a setting name and sets it to a new value, this mode ignores if the setting
    doesn't already exist
    """
    
    with transaction.manager:
        site_settings_f.set_setting(setting_name, new_value)
    
    return ""

def set_setting(setting_name, new_value):
    """
    String -> IO String
    Takes a setting name and sets it to a new value
    """
    
    the_setting = site_settings_f.get_setting(setting_name, None)
    
    if the_setting is None:
        raise Exception("No setting by that name")
    
    with transaction.manager:
        site_settings_f.set_setting(setting_name, new_value)
    
    return ""
