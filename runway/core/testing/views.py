from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
import transaction

def preview_frame(request):
    return dict()
    
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        layout      = layout,
        pre_content = pre_content,
    )
