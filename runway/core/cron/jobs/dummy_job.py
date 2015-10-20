from ....core.cron.models import CronInstance
from ....core.cron.lib import actions
import json

# _form_template = """
#   <div class="form-group">
#     <label for="time_period" class="col-sm-2 control-label">Time period</label>
#     <div class="col-sm-10">
#       {period_selector}
#     </div>
#   </div>
# """

_periods = {
    "month to date": "Month to date",
    "last month": "Last month",
    "year to date": "Year to date",
}

class DummyJob(CronInstance):
    """
    Dummy docstring which will be shown in the Cron -> Admin -> Job type page
    """
    
    job_name = "cron_dummy_job"
    job_label = "Dummy job"
    
    permissions = ["developer"]
    
    default_data = """{
        
    }"""
    
    def load(self, the_job):
        """Take a JSON string from the database and create data"""
        data = json.loads(the_job.data)
    
    def save(self):
        """Return a JSON string of the data for the database"""
        return json.dumps({})
    
    def form_render(self, request, the_job):
        return ""
    
    def form_save(self, params):
        pass
    
    def perform_job(self, the_job):
        return "Job system is working correctly", actions.no_action()
