from ....core.cron.models import CronInstance, CronLog
from ....core.cron.lib import actions
import json
import os

class RestartApplication(CronInstance):
    """
    Touches the production.ini file and causes an application restart
    """
    
    job_name = "admin_restart_application"
    job_label = "Restart site"
    
    permissions = ["su"]
    
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
        _folder_path = os.path.realpath(__file__).replace('/core/admin/jobs/restart.py', '')
        os.system("touch {}/../production.ini".format(_folder_path))
        
        return "Application restarted", actions.remove()
