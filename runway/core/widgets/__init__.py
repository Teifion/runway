def dev_views(config):
    from .views import dev
    
    config.add_route('widgets.dev.list_rwidgets', 'dev/rwidgets/list')
    
    config.add_view(dev.list_rwidgets, route_name='widgets.dev.list_rwidgets', renderer='templates/dev/list_rwidgets.pt', permission='loggedin')

def admin_views(config):
    from .views import dev
    
    config.add_route('widgets.admin.home', 'admin/home')

def user_views(config):
    from .views import user
    
    config.add_route('widgets.user.control_panel', 'user/control_panel')
    
    config.add_route('widgets.user.add_widget', 'user/add_widget')
    config.add_route('widgets.user.edit_widget', 'user/edit_widget/{widget_id}')
    config.add_route('widgets.user.remove_widget', 'user/remove_widget/{widget_id}')
    config.add_route('widgets.user.view_widget', 'user/view_widget/{widget_id}')
    
    config.add_view(user.control_panel, route_name='widgets.user.control_panel', renderer='templates/user/control_panel.pt', permission='loggedin')
    
    config.add_view(user.add_widget, route_name='widgets.user.add_widget', renderer='templates/user/add_widget.pt', permission='loggedin')
    config.add_view(user.edit_widget, route_name='widgets.user.edit_widget', renderer='templates/user/edit_widget.pt', permission='loggedin')
    config.add_view(user.remove_widget, route_name='widgets.user.remove_widget', renderer='templates/user/remove_widget.pt', permission='loggedin')
    config.add_view(user.view_widget, route_name='widgets.user.view_widget', renderer='templates/user/view_widget.pt', permission='loggedin')

def includeme(config):
    dev_views(config)
    user_views(config)
    admin_views(config)
    
    from .lib import widgets_f
    from ..hooks import append_to_hook
    
    append_to_hook("startup", widgets_f.collect_widgets)
    append_to_hook("pre_render", widgets_f.widgets_pre_render)
    
    
    from ..system.lib import auth
    auth.add("widgets", 'User', set())
    auth.add("widgets", 'Admin', {'admin'})
    auth.add("widgets", 'Super User', {'admin', 'su'}, rank=4)
    
    from .widgets import (
        example_widget,
    )
