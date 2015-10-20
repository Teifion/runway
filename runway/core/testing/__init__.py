
def includeme(config):
    from . import views
    
    config.add_route('testing.preview_frame', 'preview')
    config.add_view(views.preview_frame, route_name='testing.preview_frame', renderer='templates/preview_frame.pt', permission='developer')

