from ..models import (
    Channel,
)
from ....core.system.models.user import User
from ....core.system.lib import user_f
from ....core.base import DBSession
import transaction
from sqlalchemy.orm import aliased

_expected_jobs = {
    "system_prune_logs_job": {
        "label": "Prune logs",
        "schedule": "Every day at 1am",
        "data": json.dumps({}),
        "comments": "",
    }
}


def news_install():
    found_channels = set([j[0] for j in DBSession.query(CronJob.job).filter(CronJob.owner == 2)])
    
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

