from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
# from ..lib import user_f
from ..lib import cron_f
from ..models import CronJob, CronLog
from .. import human_time
from datetime import datetime

def home(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    recent_logs = cron_f.get_logs()
    orphaned_logs = cron_f.get_orphaned_logs()
    upcomming_jobs = cron_f.upcomming_jobs()
    
    return dict(
        title          = "Cron admin panel",
        layout         = layout,
        pre_content    = pre_content,
        
        recent_logs    = recent_logs,
        orphaned_logs = orphaned_logs,
        upcomming_jobs = upcomming_jobs,
        
        now = datetime.now(),
    )

def job_types(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    def _test_permissions(job_type):
        for p in job_type.permissions:
            if p not in request.user.permissions():
                return False
        return True
    
    job_types = filter(_test_permissions, cron_f.get_rtypes())
    
    return dict(
        title       = "Cron job types",
        layout      = layout,
        pre_content = pre_content,
        job_types   = job_types,
    )
