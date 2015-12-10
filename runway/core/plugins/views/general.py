from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ..lib import find

def home(request):
    layout      = common.render("viewer")
    
    # Make sure we're looking at an accurate list of
    # possible plugins
    # find.update_plugin_list()
    
    plugins = find.scan_for_plugins()
    
    return dict(
        title       = "Plugins: Home",
        layout      = layout,
        plugins     = plugins,
    )
