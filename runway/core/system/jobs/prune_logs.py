from ....core.cron.models import CronInstance, CronLog
from ....core.cron.lib import actions
from ....core.system.lib import logs_f
import json

from sqlalchemy import func

from ...base import DBSession
from ..models import (
    ViewLog,
    LogAggregate,
    ExceptionLog,
)

from datetime import datetime, timedelta, date
from collections import defaultdict
import transaction

class PruneLogsJob(CronInstance):
    """
    Creates the aggregate logs from daily granular logs.
    At the same time it will.
    """
    
    job_name = "system_prune_logs_job"
    job_label = "Prune logs"
    
    permissions = ["developer"]
    
    default_data = """{
        
    }"""
    
    def load(self, the_ujob):
        """Take a JSON string from the database and create data"""
        data = json.loads(the_ujob.data)
    
    def save(self):
        """Return a JSON string of the data for the database"""
        return json.dumps({})
    
    def form_render(self, request, the_job):
        return ""
    
    def form_save(self, params):
        pass
    
    def perform_job(self, the_job):
        last_job = DBSession.query(LogAggregate.date).order_by(LogAggregate.date.desc()).first()
        
        # If no aggregates have been created then instaed find the first log in our database
        if last_job is None:
            last_job = DBSession.query(ViewLog.timestamp).order_by(ViewLog.timestamp.asc()).first()[0]
        else:
            last_job = last_job[0] + timedelta(days=1)
        
        start_date = datetime(last_job.year, last_job.month, last_job.day)
        end_date = start_date + timedelta(days=1)
        
        # start_date = datetime(2015, 2, 12)
        # end_date = datetime(2015, 2, 13)
        
        # Get the logs
        logs = DBSession.query(
            ViewLog
        ).filter(
            ViewLog.timestamp >= start_date,
            ViewLog.timestamp < end_date
        )
        
        logs = list(logs)
        
        def _creator_func():
            return LogAggregate(
                page_views   = [0]*25,
                unique_users = [set() for i in range(25)],
                load_times   = [[] for i in range(25)],
            )
        
        def _add_log(the_aggregate, the_log):
            hour = the_log.timestamp.hour
            
            the_aggregate.page_views[hour] += 1
            the_aggregate.unique_users[hour].add(the_log.user)
            the_aggregate.load_times[hour].append(the_log.load_time)
            
            the_aggregate.page_views[24] += 1
            the_aggregate.unique_users[24].add(the_log.user)
            the_aggregate.load_times[24].append(the_log.load_time)
        
        aggregates = defaultdict(_creator_func)
        
        for the_log in logs:
            _add_log(aggregates['*'], the_log)
            _add_log(aggregates[the_log.section], the_log)
        
        # Flatten lists
        for section, the_aggregate in aggregates.items():
            the_aggregate.section = section
            the_aggregate.date = date(start_date.year, start_date.month, start_date.day)
            
            for hour in range(25):
                the_aggregate.unique_users[hour] = len(the_aggregate.unique_users[hour])
                the_aggregate.load_times[hour] = sum(the_aggregate.load_times[hour])/max(len(the_aggregate.load_times[hour]),1)
        
        # If no logs that day, create an empty log for the day
        if len(aggregates) == 0:
            aggregates['*'] = LogAggregate(
                section      = '*',
                date         = date(start_date.year, start_date.month, start_date.day),
                page_views   = [0]*25,
                unique_users = [0]*25,
                load_times   = [0]*25,
            )
        
        # Get some stats together for the report
        stats = {
            'total_views': aggregates['*'].page_views[24],
            'unique_views': aggregates['*'].unique_users[24],
            'load_time': aggregates['*'].load_times[24],
        }
        
        # Delete existing aggregates just incase we've got some
        with transaction.manager:
            DBSession.query(LogAggregate).filter(LogAggregate.date == date(start_date.year, start_date.month, start_date.day)).delete()
        
        # Insert the ones we've now generated
        with transaction.manager:
            for the_aggregate in aggregates.values():
                DBSession.add(the_aggregate)
        
        # Prune older logs, incuding job logs!
        delete_log_date = start_date - timedelta(days=5)
        with transaction.manager:
            stats['prunned_view_logs'] = DBSession.query(func.count(ViewLog.id)).filter(ViewLog.timestamp < delete_log_date).first()[0]
            stats['prunned_job_logs'] = DBSession.query(func.count(CronLog.id)).filter(CronLog.end_time < delete_log_date).first()[0]
            
            DBSession.query(ViewLog).filter(ViewLog.timestamp < delete_log_date).delete()
            DBSession.query(CronLog).filter(CronLog.end_time < delete_log_date).delete()
        
        the_report = """Created aggregate for {the_date}<br />
Total views: {total_views}<br />
Unique views: {unique_views}<br />
Load time: {load_time}<br />
<br />
Prunned view logs: {prunned_view_logs}<br />
Prunned job logs: {prunned_job_logs}""".format(
            the_date = start_date.strftime("%d/%m/%Y"),
            total_views = stats['total_views'],
            unique_views = stats['unique_views'],
            load_time = round(stats['load_time'],2),
            
            prunned_view_logs = stats['prunned_view_logs'],
            prunned_job_logs = stats['prunned_job_logs'],
        )
        
        # If we're still behind time then re-schedule for right now
        if end_date + timedelta(days=1) < datetime.now():
            return the_report, actions.resubmit(datetime.now())
        
        # Not behind
        return the_report


'''
UPDATE runway_logs SET section = LEFT(REPLACE(path, '/hwifs/', ''), POSITION('/' in REPLACE(path, '/hwifs/', ''))) WHERE section = 'hwifs';
UPDATE runway_logs SET section = REPLACE(section, '/', '');

DROP TABLE runway_log_aggregate_sections;
DROP TABLE runway_log_aggregates;

DROP TABLE runway_cron_job_logs;
DROP TABLE runway_cron_jobs;
'''