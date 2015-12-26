from ....core.commands.lib import funcs
from ....core.cli.lib import cli_f
from ....core.system.lib import site_settings_f
from ..lib import themes_f
import transaction
from ...base import DBSession
from ...system.models.user import (
    User,
)

def change_theme(theme_name):
    """
    String -> ()
    Takes in theme name and changes the selected theme to that
    """
    
    name_list = [t.name for t in themes_f.get_themes()]
    
    with transaction.manager:
        if theme_name in name_list:
            themes_f._write_theme(theme_name)
            site_settings_f.set_setting("runway.themes.site_theme", theme_name)
            return cli_f.shell_text("[g]Success: Theme changed[/g]")
        else:
            return cli_f.shell_text("[r]Error: No theme named {}[/r]".format(theme_name))

def list_themes():
    """
    () -> IO String
    Prints a list of themes in the system
    """
    name_list = [t.name for t in themes_f.get_themes()]
    
    return "\n".join(name_list)
