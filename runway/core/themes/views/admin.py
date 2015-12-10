from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ....core.lib import common
from ....core.system.lib import user_f, site_settings_f
from pyramid.renderers import get_renderer
from ..lib import themes_f

def home(request):
    layout      = common.render("viewer")
    
    site_theme = site_settings_f.get_setting("runway.themes.site_theme")
    themes = themes_f.get_themes()
    
    return dict(
        title       = "Themes admin",
        layout      = layout,
        
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
    
    return dict(
        title       = "Switch theme",
        layout      = layout,
        theme_name  = theme_name,
    )

def view_theme(request):
    theme_name = request.matchdict['theme_name']
    
    layout = get_renderer('../../../themes/{}/viewer.pt'.format(theme_name)).implementation()
    
    return dict(
        title       = "View theme",
        layout      = layout,
    )
