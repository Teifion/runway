from ...base import DBSession
from ..models import UserWidget
from ...system.models.user import User
from datetime import datetime
import json
from sqlalchemy import func

import sys
import transaction

def install():
    root_widget_count = DBSession.query(
        func.count(UserWidget.id)
    ).filter(
        UserWidget.user == 1
    ).first()[0]
    
    if root_widget_count == 0:
        with transaction.manager:
            # Root has no widgets, lets give them two basic ones as defaults
            DBSession.add(UserWidget(
                user = 1,
                widget = "dev_errors_widget",
                label = "Exception count",
                data = "{}",
            ))
            
            DBSession.add(UserWidget(
                user = 1,
                widget = "dev_server_load_widget",
                label = "Server load",
                data = "{}",
            ))
    
    # for job, data in expected_jobs.items():
    #     if job in found_jobs: continue
        
    #     gen = human_time.parse(data['schedule'])
        
    #     with transaction.manager:
    #         DBSession.add(CronJob(
    #             owner         = 2,
                
    #             label         = data['label'],
    #             job           = job,
                
    #             # Set to null when job is disabled/paused
    #             next_run      = next(gen),
                
    #             # Schedule is passed to human time, schedule_start means we can combine multiple times without it causing an issue
    #             schedule       = data['schedule'],
    #             schedule_start = datetime.now(),
                
    #             data          = data['data'],
    #             comments      = data['comments'],
    #         ))

