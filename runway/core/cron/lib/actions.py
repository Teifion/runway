"""
A set of functions for creating "actions" for execution after
a cron job has completed. Each action is just a function executing
with the sole argument for the action being the job completed.

Note: These are not the same as trigger actions and are not
visible to end-users, only to developers.
"""

from ...base import DBSession
from ..models import CronJob
import transaction

def no_action():
    def f(the_job):
        pass
    
    return f

def resubmit(new_date):
    def f(the_job):
        with transaction.manager:
            the_job.next_run = new_date
            DBSession.add(the_job)
    
    return f

def orphan_logs():
    def f(the_job):
        with transaction.manager:
            stmt = "UPDATE runway_cron_job_logs SET job = Null WHERE job = :id"
            args = dict(
                id     = the_job.id,
            )
            
            DBSession.execute(stmt, args)
            DBSession.execute("COMMIT")
    return f
        

def remove():
    def f(the_job):
        with transaction.manager:
            stmt = "DELETE FROM runway_cron_job_logs WHERE job = :id"
            args = dict(
                id     = the_job.id,
            )
            
            DBSession.execute(stmt, args)
            
            # Now delete the job
            stmt = "DELETE FROM runway_cron_jobs WHERE id = :id"
            args = dict(
                id     = the_job.id,
            )
            
            DBSession.execute(stmt, args)
            DBSession.execute("COMMIT")
    return f

def one_off():
    """
    It pauses the job.
    
    Used for a job which should not be re-run automatically, ever.
    """
    def f(the_job):
        with transaction.manager:
            the_job.next_run = None
            DBSession.add(the_job)
    return f
