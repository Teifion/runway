from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
# from ..lib import user_f
from ..lib import cron_f
# from ..models import CronJob, CronLog
from .. import human_time
from datetime import datetime

def view(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    log_id = int(request.matchdict['log_id'])
    the_log, the_job, the_user = cron_f.get_log(log_id)
    
    return dict(
        title       = "View log",
        layout      = layout,
        pre_content = pre_content,
        
        the_log  = the_log,
        the_job  = the_job,
        the_user = the_user,
    )

def view_for_job(request):
    pass

def view_for_user(request):
    pass

def view_for_time(request):
    pass
