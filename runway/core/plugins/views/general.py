from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ..lib import find

def home(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    # Make sure we're looking at an accurate list of
    # possible plugins
    # find.update_plugin_list()
    
    plugins = find.scan_for_plugins()
    
    return dict(
        title       = "Plugins: Home",
        layout      = layout,
        pre_content = pre_content,
        plugins     = plugins,
    )
