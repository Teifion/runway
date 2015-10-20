from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
# from ..lib import user_f
from ..lib import widgets_f
from ..models import UserWidget

def control_panel(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    user_widgets = widgets_f.get_uwidgets(request.user.id)
    
    return dict(
        title       = "User control panel",
        layout      = layout,
        pre_content = pre_content,
        message     = message,
        
        user_widgets = user_widgets,
        widget_types = {t.widget_name:t.widget_label for t in widgets_f.get_rtypes()},
    )

def add_widget(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    if "widget_label" in request.params:
        the_type = widgets_f.get_rwidget_type(request.params['widget_type'])
        
        w = UserWidget(
            user             = request.user.id,
            widget           = request.params['widget_type'],
            label            = request.params['widget_label'],
            data             = the_type.default_data,
        )
        widget_id = widgets_f.save(w, return_id=True)
        return HTTPFound(request.route_url('widgets.user.edit_widget', widget_id=widget_id))
    
    def _test_permissions(widget_type):
        for p in widget_type.permissions:
            if p not in request.user.permissions():
                return False
        return True
    
    widget_types = {t.widget_name:t.widget_label for t in filter(_test_permissions, widgets_f.get_rtypes())}
    
    return dict(
        title       = "Add widget",
        layout      = layout,
        pre_content = pre_content,
        message     = message,
        
        widget_type_select = common.select_box("widget_type", widget_types),
    )

def edit_widget(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    the_uwidget = widgets_f.get_uwidget(int(request.matchdict['widget_id']))
    the_rwidget = widgets_f.get_rwidget(the_uwidget)
    
    if "widget_label" in request.params:
        the_uwidget.label = request.params['widget_label']
        the_rwidget.form_save(request.params)
        widgets_f.save(the_uwidget, the_rwidget)
    
    widget_types = {t.widget_name:t.widget_label for t in widgets_f.get_rtypes()}
    
    return dict(
        title       = "Edit widget",
        layout      = layout,
        pre_content = pre_content,
        message     = message,
        
        the_uwidget = the_uwidget,
        widget_type_select = common.select_box("widget_type", widget_types, selected=the_uwidget.widget, disabled="disabled"),
        
        form_render = the_rwidget.form_render(request, the_uwidget),
        view_render = the_rwidget.view_render(request, the_uwidget),
        
        js_libs = the_rwidget.js_libs,
        css_libs = the_rwidget.css_libs,
    )

def remove_widget(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    widget_id = int(request.matchdict['widget_id'])
    
    if int(request.params.get('confirm', '-1')) == widget_id:
        widgets_f.delete_uwidget(widget_id)
        return HTTPFound(request.route_url('widgets.user.control_panel'))
    
    return dict(
        title       = "Remove widget",
        layout      = layout,
        pre_content = pre_content,
        message     = message,
        
        widget_id = widget_id,
    )

def view_widget(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    return dict(
        title       = "View widget",
        layout      = layout,
        pre_content = pre_content,
        message     = message,
    )
