from ...base import DBSession
from ...system.models.user import User

from collections import namedtuple
from ..models import CronJob, CronLog, CronInstance
from sqlalchemy import and_, or_
from .. import human_time
from ...system.lib import errors_f, render_f
from ...system.models.user import User
from datetime import datetime

import sys
import transaction

_jobs = {}
get_rtypes = _jobs.values

def register(the_job):
    _jobs[the_job.name] = the_job

def collect_instances():
    for c in CronInstance.__subclasses__():
        _jobs[c.job_name] = c

def get_instance(job_name):
    return _jobs[job_name]

def create_instance(the_job):
    TheType = get_instance(the_job.job)
    the_instance = TheType()
    the_instance.load(the_job)
    return the_instance


def get_job(job_id):
    return DBSession.query(CronJob).filter(CronJob.id == job_id).first()

def get_jobs(user_id):
    return DBSession.query(CronJob).filter(CronJob.owner == user_id).order_by(CronJob.next_run.asc())

def upcomming_jobs(limit=20):
    # Jobs which have yet to run
    return DBSession.query(
        CronJob,
        User
    ).join(
        (User, User.id == CronJob.owner),
    ).order_by(CronJob.next_run.asc()).limit(limit)

def get_log(log_id):
    return DBSession.query(
        CronLog,
        CronJob,
        User,
    ).join(
        (User, and_(User.id == CronLog.runner)),
    ).outerjoin(
        (CronJob, and_(CronJob.id == CronLog.job)),
    ).filter(
        CronLog.id == log_id,
    ).order_by(
        CronLog.end_time.desc()
    ).first()

def get_logs(user_id=None, job_id=None, page=1):
    return DBSession.query(
        CronLog,
        CronJob,
        User,
    ).join(
        (CronJob, and_(CronJob.id == CronLog.job)),
        (User, and_(User.id == CronLog.runner)),
    ).filter(
        or_(CronLog.runner == user_id, CronJob.owner == user_id) if user_id != None else True,
        CronLog.job == job_id if job_id != None else True,
    ).order_by(
        CronLog.end_time.desc()
    ).limit(20).offset((page-1)*20)

def get_orphaned_logs(user_id=None, page=1):
    return DBSession.query(
        CronLog,
        User,
    ).join(
        (User, and_(User.id == CronLog.runner)),
    ).filter(
        or_(CronLog.runner == user_id, CronJob.owner == user_id) if user_id != None else True,
        CronLog.job == None,
    ).order_by(
        CronLog.end_time.desc()
    ).limit(20).offset((page-1)*20)

def delete_job(job_id):
    DBSession.query(CronLog).filter(CronLog.job == job_id).delete()
    DBSession.query(CronJob).filter(CronJob.id == job_id).delete()

def save(the_job, the_instance=None, return_id=False):
    if the_instance != None:
        the_job.data = the_instance.save()
    
    p = DBSession.add(the_job)
    
    if return_id:
        return DBSession.query(CronJob.id).filter(CronJob.label == the_job.label).order_by(CronJob.id.desc()).first()[0]

def get_next_run(schedule, schedule_start):
    gen = human_time.parse(schedule, schedule_start)
    now = datetime.now()
    
    # Keep generating until we get to the next acceptable one
    v = next(gen)
    while v <= now:
        v = next(gen)
    
    return v

def check_permission(the_user, owner):
    if the_user.id == owner:
        return True
    
    if owner > 2:
        if "cron.admin" in the_user.permissions():
            return True
    else:
        if "cron.su" in the_user.permissions():
            return True
    
    return False

def run_job(the_job, runner=2):
    job_id = int(the_job.id)
    
    start_time = datetime.now()
    
    # First, is it locked?
    if _check_if_locked(the_job.id):
        add_log(runner, the_job.id, start_time, datetime.now(), "Locked", "")
        return "Cancelled"
    
    # Nope? Lock it
    _lock_job(the_job)
    
    with transaction.manager:
        the_instance = create_instance(the_job)
        try:
            job_results = the_instance.perform_job(the_job)
            DBSession.execute("COMMIT")
        except Exception as e:
            DBSession.execute("ROLLBACK")
            
            the_job = get_job(job_id)
            
            # Log it as an actual exception
            errors_f.log_error_without_request(sys.exc_info(), runner, path="cron.run_job()", description=e.args[0], context=5)
            
            # Show the log as an error too
            add_log(runner, the_job.id, start_time, datetime.now(), "Exception", errors_f.html_render(sys.exc_info(), context=5))
            
            _pause_job(the_job)
            _unlock_job(the_job)
            return "Exception"
    
    # If not a sequence we'll pretend it was for the next bit
    if isinstance(job_results, str):
        job_results = [job_results]
    
    # Get report and get actions
    job_report = job_results[0]
    job_actions = job_results[1:]
    
    the_job = get_job(job_id)
    if _check_if_locked(the_job.id):
        if job_report is None: job_report = ""
        add_log(runner, the_job.id, start_time, datetime.now(), "Success", job_report)
    
    # Unlock and set next run time
    _set_next_run_time(the_job)
    _unlock_job(the_job)
    
    # Now perform actions
    for a in job_actions:
        a(the_job)

def _check_if_locked(job_id):
    result = DBSession.query(CronJob.locked).filter(CronJob.id == job_id).first()
    if result is None:
        raise KeyError("Job not found")
    return result[0]

def _lock_job(the_job):
    with transaction.manager:
        stmt = "UPDATE runway_cron_jobs SET locked = :locked WHERE id = :id"
        args = dict(
            locked = datetime.now(),
            id     = the_job.id,
        )
        
        DBSession.execute(stmt, args)
        DBSession.execute("COMMIT")

def _unlock_job(the_job):
    with transaction.manager:
        stmt = "UPDATE runway_cron_jobs SET locked = :locked WHERE id = :id"
        args = dict(
            locked = None,
            id     = the_job.id,
        )
        
        DBSession.execute(stmt, args)
        DBSession.execute("COMMIT")

def _pause_job(the_job):
    with transaction.manager:
        stmt = "UPDATE runway_cron_jobs SET next_run = :next_run WHERE id = :id"
        args = dict(
            next_run = None,
            id       = the_job.id,
        )
        
        DBSession.execute(stmt, args)
        DBSession.execute("COMMIT")

def _set_next_run_time(the_job):
    with transaction.manager:
        stmt = "UPDATE runway_cron_jobs SET next_run = :next_run WHERE id = :id"
        args = dict(
            next_run = get_next_run(the_job.schedule, the_job.schedule_start),
            id       = the_job.id,
        )
        
        DBSession.execute(stmt, args)
        DBSession.execute("COMMIT")

def add_log(runner, job_id, start_time, end_time, status, report):
    """We are adding it manually because when running the job itself
    we use transactions and exceptions manually to give more
    fine grained control over how it runs"""
    
    with transaction.manager:
        stmt = """INSERT INTO runway_cron_job_logs
            (runner, job, start_time, end_time, status, report) VALUES
            (:runner, :job, :start_time, :end_time, :status, :report);"""
        
        args = dict(
            runner     = runner,
            job        = job_id,
            start_time = start_time,
            end_time   = end_time,
            status     = status,
            report     = report,
        )
        
        # For some reason it won't let us use DBSession.add()
        # I would assume this is because we're breaking out
        # of the normal transaction block
        DBSession.execute(stmt, args)
        DBSession.execute("COMMIT")

def get_pending_jobs(limit=None):
    return DBSession.query(
        CronJob
    ).filter(
        CronJob.locked == None,
        CronJob.next_run <= datetime.now(),
    ).order_by(
        CronJob.next_run.asc()
    ).limit(limit)

def background_process():
    # from pyramid.paster import bootstrap
    
    # env = bootstrap('{}/production.ini'.format(config['dev_path']))
    
    # Check for duplicated jobs before running
    # with transaction.manager:
    #     DBSession.execute("""UPDATE runway_cron_jobs
    #         SET time_taken = -3, completed = '2013/01/01'
    #             WHERE id IN (SELECT wj1.id
    #                 FROM worker_jobs AS wj1, worker_jobs AS wj2
    #                     WHERE wj1.submitter = wj2.submitter
    #                     AND wj1.data = wj2.data
    #                     AND wj1.name = wj2.name
    #                     AND wj1.submitter = wj2.submitter
    #                     AND date_trunc('minute', wj1.submitted) = date_trunc('minute', wj2.submitted)
    #                     AND wj1.id < wj2.id
    #                     AND wj1.completed is Null AND wj2.completed is Null);""")
    #     DBSession.execute("COMMIT")
    
    job_list = tuple(get_pending_jobs())
    for j in job_list:
        run_job(j, runner=2)

def cron_pre_render(request):
    display_flag = any((request.runway_settings.users['allow_cron'] == 'True',
        'cron' in request.user.permissions()
    ))
    
    if display_flag:
        request.render['user_links'].append(
            render_f.dropdown_menu_item("", "", "clock-o", "Cron jobs", request.route_url('cron.user.control_panel'))
        )
