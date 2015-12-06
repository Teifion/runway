from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ....core.lib import common
from ....core.system.lib import user_f, site_settings_f
from pyramid.renderers import get_renderer
from ..lib import themes_f

def home(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    site_theme = site_settings_f.get_setting("runway.themes.site_theme")
    themes = themes_f.get_themes()
    
    return dict(
        title       = "Themes admin",
        layout      = layout,
        pre_content = pre_content,
        
        site_theme  = site_theme,
        themes      = themes,
    )

def select_theme(request):
    theme_name = request.matchdict['theme_name']
    name_list = [t.name for t in themes_f.get_themes()]
    
    if theme_name in name_list:
        themes_f._write_theme(theme_name)
        site_settings_f.set_setting("runway.themes.site_theme", theme_name)
        
    else:
        raise KeyError("Theme of '{}' does not exist".format(theme_name))
    
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title       = "Switch theme",
        layout      = layout,
        pre_content = pre_content,
        theme_name  = theme_name,
    )

def view_theme(request):
    theme_name = request.matchdict['theme_name']
    
    layout = get_renderer('../../../themes/{}/viewer.pt'.format(theme_name)).implementation()
    pre_content = get_renderer('../../../themes/{}/general_menu.pt'.format(theme_name)).implementation()
    
    return dict(
        title       = "View theme",
        layout      = layout,
        pre_content = pre_content,
    )