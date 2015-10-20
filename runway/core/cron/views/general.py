from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
# from ..lib import user_f
from ..lib import cron_f
from ..models import CronJob, CronLog
from .. import human_time
from datetime import datetime

def control_panel(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    user_jobs = cron_f.get_jobs(request.user.id)
    user_logs = cron_f.get_logs(request.user.id)
    
    return dict(
        title       = "User control panel",
        layout      = layout,
        pre_content = pre_content,
        message     = message,
        
        user_jobs   = user_jobs,
        user_logs   = user_logs,
        
        job_types = {t.job_name:t.job_label for t in cron_f.get_rtypes()},
    )

def create(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    if "job_label" in request.params and "job_type" in request.params:
        the_type = cron_f.get_instance(request.params['job_type'])
        
        j = CronJob(
            owner = request.user.id,
            job   = request.params['job_type'],
            label = request.params['job_label'],
            next_run = None,
            last_run = None,
            schedule = "",
            data  = the_type.default_data,
        )
        job_id = cron_f.save(j, return_id=True)
        return HTTPFound(request.route_url('cron.user.edit', job_id=job_id))
    
    def _test_permissions(job_type):
        for p in job_type.permissions:
            if p not in request.user.permissions():
                return False
        return True
    
    job_types = {t.job_name:t.job_label for t in filter(_test_permissions, cron_f.get_rtypes())}
    
    return dict(
        title       = "Create new job",
        layout      = layout,
        pre_content = pre_content,
        message     = message,
        
        job_type_select = common.select_box("job_type", job_types),
    )

def edit(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    the_job = cron_f.get_job(int(request.matchdict['job_id']))
    the_instance = cron_f.create_instance(the_job)
    
    if not cron_f.check_permission(request.user, the_job.owner):
        return HTTPFound(request.route_url('cron.user.control_panel'))
    
    if "job_label" in request.params:
        the_job.label = request.params['job_label']
        the_job.schedule = request.params['schedule'].strip()
        the_job.schedule_start = datetime.now()
        the_job.comments = request.params['comments']
        
        if the_job.schedule == "":
            the_job.next_run = None
        else:
            # Work out when we're next running it
            the_job.next_run = cron_f.get_next_run(the_job.schedule, the_job.schedule_start)
        
        the_instance.form_save(request.params)
        cron_f.save(the_job, the_instance)
        
        message = "success", "Changes saved"
    
    def _test_permissions(job_type):
        for p in job_type.permissions:
            if p not in request.user.permissions():
                return False
        return True
    
    job_types = {t.job_name:t.job_label for t in filter(_test_permissions, cron_f.get_rtypes())}
    
    return dict(
        title               = "Edit job",
        layout              = layout,
        pre_content         = pre_content,
        message             = message,
        
        the_job             = the_job,
        job_type_select     = common.select_box("job_type", job_types, selected=the_job.job, disabled="disabled"),
        
        now                 = datetime.now(),
        form_render         = the_instance.form_render(request, the_job),
    )

def delete(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    job_id = int(request.matchdict['job_id'])
    the_job = cron_f.get_job(int(request.matchdict['job_id']))
    
    if not cron_f.check_permission(request.user, the_job.owner):
        return HTTPFound(request.route_url('cron.user.control_panel'))
    
    if int(request.params.get('confirm', '-1')) == job_id:
        cron_f.delete_job(job_id)
        return HTTPFound(request.route_url('cron.user.control_panel'))
    
    return dict(
        title       = "Remove job",
        layout      = layout,
        pre_content = pre_content,
        message     = message,
        
        job_id = job_id,
    )

def run(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    job_id = int(request.matchdict['job_id'])
    the_job = cron_f.get_job(int(request.matchdict['job_id']))
    
    if not cron_f.check_permission(request.user, the_job.owner):
        return HTTPFound(request.route_url('cron.user.control_panel'))
    
    if int(request.params.get('confirm', '-1')) == job_id:
        the_job.next_run = datetime.now()
        cron_f.save(the_job)
        return HTTPFound(request.route_url('cron.user.control_panel'))
    
    return dict(
        title       = "Run job",
        layout      = layout,
        pre_content = pre_content,
        
        job_id = job_id,
    )

def run_now(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    job_id = int(request.matchdict['job_id'])
    the_job = cron_f.get_job(int(request.matchdict['job_id']))
    
    if not cron_f.check_permission(request.user, the_job.owner):
        return HTTPFound(request.route_url('cron.user.control_panel'))
    
    if int(request.params.get('confirm', '-1')) == job_id:
        cron_f.run_job(the_job, runner=request.user.id)
        return HTTPFound(request.route_url('cron.user.control_panel'))
    
    return dict(
        title       = "Run job",
        layout      = layout,
        pre_content = pre_content,
        
        job_id = job_id,
    )

def pause(request):
    job_id = int(request.matchdict['job_id'])
    the_job = cron_f.get_job(int(request.matchdict['job_id']))
    
    if not cron_f.check_permission(request.user, the_job.owner):
        return HTTPFound(request.route_url('cron.user.control_panel'))
    
    the_job.next_run = None
    cron_f.save(the_job)
    return HTTPFound(request.route_url('cron.user.control_panel'))

def resume(request):
    job_id = int(request.matchdict['job_id'])
    the_job = cron_f.get_job(int(request.matchdict['job_id']))
    
    if not cron_f.check_permission(request.user, the_job.owner):
        return HTTPFound(request.route_url('cron.user.control_panel'))
    
    the_job.next_run = cron_f.get_next_run(the_job.schedule, the_job.schedule_start)
    cron_f.save(the_job)
    return HTTPFound(request.route_url('cron.user.control_panel'))

def unlock(request):
    job_id = int(request.matchdict['job_id'])
    the_job = cron_f.get_job(int(request.matchdict['job_id']))
    
    if not cron_f.check_permission(request.user, the_job.owner):
        return HTTPFound(request.route_url('cron.user.control_panel'))
    
    the_job.locked = None
    cron_f.save(the_job)
    return HTTPFound(request.route_url('cron.user.edit', job_id=the_job.id))

def human_time_view(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title       = "Human time",
        layout      = layout,
        pre_content = pre_content,
    )

def human_time_test(request):
    text = request.params['text']
    result_format = request.params.get('format', 'html')
    limit = int(request.params.get('limit', 3))
    
    gen = human_time.parse(text)
    result = [next(gen).strftime("%A %d/%m/%Y %H:%M:%S") for x in range(limit)]
    
    if result_format == "html":
        return "<br />".join(result)
    else:
        raise Exception("No handler for format of '{}'".format(result_format))
    
    return text