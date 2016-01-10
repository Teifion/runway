import os
import re
import importlib
from pyramid.renderers import get_renderer
from ....core.system.lib import site_settings_f

_folder_path = os.path.realpath(__file__).replace('/core/themes/lib/themes_f.py', '/themes')
_folder_name = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_]+$')

_selected_theme = [""]

def render(part_name):
    return get_renderer('../../../themes/{}/{}.pt'.format(_selected_theme[0], part_name)).implementation()

def _startup():
    try:
        _selected_theme[0] = site_settings_f.get_setting("runway.themes.site_theme")
    except Exception:
        pass
    
    # print("\n\n")
    # for t in scan_themes_folder():
    #     the_theme = import_theme(t)
        
    #     print(the_theme.name)
    #     print(the_theme.label)
    # print("\n\n")
    # print(list(get_themes()))
    # _clean_theme_folder()
    # _write_theme("sb_admin_v2")
    pass

def _clean_theme_folder():
    os.system('find "{}/_selected" -name "*.pt" -exec rm {{}} \;'.format(_folder_path))

def _write_theme(theme_name):
    _selected_theme[0] = theme_name
    # _clean_theme_folder()
    # cmd = 'cp -R "{folder}/{theme_name}/" "{folder}/_selected";'.format(folder=_folder_path, theme_name=theme_name)
    # os.system(cmd)
    
def scan_themes_folder():
    listdir = os.listdir(_folder_path)
    
    for f in listdir:
        if _folder_name.search(f):
            yield f

def get_themes():
    return map(import_theme, scan_themes_folder())

def import_theme(theme_name):
    from . import theme_holder
    
    exec("from ....themes import %s" % theme_name, theme_holder.__dict__)
    
    result = theme_holder.__dict__[theme_name]
    del(theme_holder.__dict__[theme_name])
    
    return result
