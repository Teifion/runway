from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
# from ..lib import user_f
from ..lib import widgets_f
from ..models import UserWidget

def list_rwidgets(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    widget_names = list(widgets_f._widgets.keys())
    widget_names.sort()
    
    
    return dict(
        title       = "Developer: Widgets",
        layout      = layout,
        pre_content = pre_content,
        message     = message,
        
        widgets     = map(widgets_f.get_rwidget_type, widget_names),
    )
