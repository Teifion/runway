from pyramid.httpexceptions import HTTPFound
from ...lib import common

from ....core.system.js_widgets import UserPicker
from ...cron.models import CronJob
from ...cron.lib import cron_f
from ...system.lib import site_settings_f
from ..lib import stats_f, admin_f
from datetime import datetime

def home(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    UserPicker(request)
    
    request.add_documentation("admin.user")
    request.add_documentation("admin.settings")
    
    sections = admin_f.get_sections()
    
    return dict(
        title       = "Admin: Home",
        layout      = layout,
        pre_content = pre_content,
    )

def settings(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    settings_dict = site_settings_f.get_all_settings()
    
    if "change" in request.params:
        for group_name, group_settings in site_settings_f._settings_structure:
            for k, permission, _, data_type, default, __ in group_settings:
                if permission != "" and permission not in request.user.permissions():
                    continue
                
                if data_type == "boolean":
                    v = "True" if k in request.params else "False"
                else:
                    v = request.params[k]
                
                if v != str(settings_dict.get(k)):
                    site_settings_f.set_setting(k, v)
                    settings_dict[k] = v
        
        if "admin.su" in request.user.permissions():
            message = "success", """Settings succesfully changed. Some settings may require a restart to take effect.
                <br /><br />
                
                <a href="{}" class="btn btn-default">Schedule restart</a>
                """.format(request.route_url("admin.schedule_restart"))
        else:
            message = "success", "Settings succesfully changed. Some settings may require a restart to take effect."
            
    
    return dict(
        title          = "Admin: Settings",
        layout         = layout,
        pre_content    = pre_content,
        settings_dict  = settings_dict,
        setting_groups = site_settings_f._settings_structure,
        message        = message,
    )

def site_stats(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    stats = {
        "core": stats_f.get_stats()
    }
    
    return dict(
        title       = "Admin: Site stats",
        layout      = layout,
        pre_content = pre_content,
        
        stats       = stats,
    )
    
def schedule_restart(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    if "date" in request.params:
        the_date = request.params['date']
        the_time = request.params['time']
        
        the_datetime = common.string_to_datetime("{}T{}:00".format(the_date, the_time))
        
        if the_datetime != None:
            j = CronJob(
                owner = request.user.id,
                job   = "admin_restart_application",
                label = "Scheduled restart",
                next_run = the_datetime,
                last_run = None,
                schedule = "",
                data  = "{}",
            )
            job_id = cron_f.save(j, return_id=True)
            return HTTPFound(request.route_url('cron.user.edit', job_id=job_id))
        
    
    return dict(
        title       = "Admin: Schedule restart",
        layout      = layout,
        pre_content = pre_content,
        
        now         = datetime.now(),
    )
