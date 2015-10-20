from ...base import DBSession
from ..models import CronJob
from ...system.models.user import User
from datetime import datetime
from .. import human_time
import json

import sys
import transaction

_expected_jobs = {
    "system_prune_logs_job": {
        "label": "Prune logs",
        "schedule": "Every day at 1am",
        "data": json.dumps({}),
        "comments": "",
    }
}

def install_jobs():
    """
    This is a function which can be used by other modules to ensure certain jobs
    are created automatically to be run by a system process. If you want to
    have jobs be placed under a specific user you will need to do it within the
    module itself as there are more variables to consider.
    """
    
    install(_expected_jobs)

def install(expected_jobs):
    found_jobs = set([j[0] for j in DBSession.query(CronJob.job).filter(CronJob.owner == 2)])
    
    for job, data in expected_jobs.items():
        if job in found_jobs: continue
        
        gen = human_time.parse(data['schedule'])
        
        with transaction.manager:
            DBSession.add(CronJob(
                owner         = 2,
                
                label         = data['label'],
                job           = job,
                
                # Set to null when job is disabled/paused
                next_run      = next(gen),
                
                # Schedule is passed to human time, schedule_start means we can combine multiple times without it causing an issue
                schedule       = data['schedule'],
                schedule_start = datetime.now(),
                
                data          = data['data'],
                comments      = data['comments'],
            ))

