# from ....core.cron.models import CronInstance, CronLog
# from ....core.cron.lib import actions
# from ....core.system.lib import logs_f
# import json

# from sqlalchemy import func

# from ...base import DBSession
# from ..models import (
#     ViewLog,
#     LogAggregate,
#     ExceptionLog,
# )

# from ..lib import backup_f

# class BackupDatabase(CronInstance):
#     """
#     Creates the aggregate logs from daily granular logs.
#     At the same time it will.
#     """
    
#     job_name = "system_backup_database"
#     job_label = "Backup system database"
    
#     permissions = ["developer"]
    
#     default_data = """{
        
#     }"""
    
#     def load(self, the_ujob):
#         """Take a JSON string from the database and create data"""
#         data = json.loads(the_ujob.data)
    
#     def save(self):
#         """Return a JSON string of the data for the database"""
#         return json.dumps({})
    
#     def form_render(self, request, the_job):
#         return ""
    
#     def form_save(self, params):
#         pass
    
#     def perform_job(self, the_job):
#         backup_f.perform_backup()
        
#         the_report = "Report of what's what"
        
#         return the_report
