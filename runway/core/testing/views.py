from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
import transaction

def preview_frame(request):
    return dict()
    
    layout      = common.render("viewer")
    
    return dict(
        layout      = layout,
    )
