from pyramid.httpexceptions import HTTPFound
from ...lib import common
import transaction

# from ...base import DBSession
from ..models.user import User
from ...admin.lib import admin_f
from ..lib import site_settings_f, user_f
from ...widgets.lib import widgets_f

def root(request):
    layout      = common.render("viewer")
    
    uwidgets = tuple(widgets_f.get_uwidgets(request.user.id))
    rwidgets = tuple(map(widgets_f.get_rwidget, uwidgets))
    ur_list = tuple(zip(uwidgets, rwidgets))
    
    renders = []
    js_libs = []
    css_libs = []
    
    if request.runway_settings.users['allow_widgets'] == 'True' or 'widgets' in request.user.permissions():
        for the_uwidget, the_rwidget in ur_list:
            renders.append(the_rwidget.view_render(request, the_uwidget))
            
            for j in the_rwidget.js_libs:
                if j not in js_libs:
                    js_libs.append(j)
            
            for c in the_rwidget.css_libs:
                if c not in css_libs:
                    css_libs.append(c)
    
    messages = site_settings_f.get_settings("runway.system.dev_message", "runway.system.admin_message")
    
    # request.messages = [
    #     ('#', 'Competition for today', 'First to 4 policies', 'The first person to 4 policies gets a half hour extension to their lunch. 2nd, 3rd and 4th place get an extra 15 minutes to theirs.'),
    #     ('#', 'Compliance update', 'Less to say!', 'From today we are using the new, shorter, smoking script.'),
    # ]
    
    # request.tasks = [
    #     ('#', 'Audits fed back', 89, "success"),
    #     ('#', 'Monthly 1-2-1s', 45, "warning"),
    #     ('#', 'Audits performed', 20, "danger"),
    # ]
    
    # request.user_links = [
    #     ('#', 'gear', 'Settings'),
    # ]
    
    # request.alerts = [
    #     ('#', 'phone', 'Pierce Hawthorne got a sale', 'Just now'),
    #     ('#', 'headphones', 'Audit for Dean Pelton', '12 minutes ago'),
    #     ('#', 'phone', 'Yahtzee Croshaw got a sale', '36 minutes ago'),
    #     ('#', 'bar-chart-o', 'End of week report published', '4 hours ago'),
    # ]
    
    return dict(
        title       = "Home",
        layout      = layout,
        
        messages    = messages,
        renders     = renders,
        
        js_libs     = js_libs,
        css_libs    = css_libs,
    )

def register(request):
    if site_settings_f.get_setting("runway.users.allow_registration", False) != "True":
        return HTTPFound(request.route_url("/"))
    
    if hasattr(request, "user"):
        return HTTPFound(request.route_url("/"))
    
    success = False
    new_username = ""
    
    if "display_name" in request.params:
        new_user = user_f.blank_user()
        new_user.display_name = request.params["display_name"].strip()
        new_user.username = admin_f.new_username(new_user.display_name)
        new_user.initials = admin_f.new_initials(new_user.display_name)
        
        password1 = request.params['password1']
        password2 = request.params['password2']
        
        if len(password1) < 8:
            raise common.GracefulException("Inadequate password", """Your password must be at least 8 characters long.""",
                category="Input")
        
        if password1 != "":
            if password1 != password2:
                raise common.GracefulException("Mismatched passwords", """The confirmation password does not match the intial password.""",
                category="Input")
        
        # Save the password
        new_user.new_password(password1)
        
        # Get the ID
        user_f.add_user(new_user)
        new_username = new_user.username
        success = True
    
    layout = common.render("blank")
    
    return dict(
        title        = "Registration",
        layout       = layout,
        success      = success,
        new_username = new_username,
    )

def up(request):
    return "Site is up"
