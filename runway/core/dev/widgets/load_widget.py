from ....core.widgets.models import RunwayWidget
from ....core.lib import common
from ..lib import exceptions_f
import json
import os

_form_template = """
  <div class="form-group">
    <label for="time_period" class="col-sm-2 control-label">Time period</label>
    <div class="col-sm-10">
      {period_selector}
    </div>
  </div>
"""

_view_template = """
  <div>
    <div class="alert alert-{status} alert-dismissible" role="alert">
      <button type="button" class="close" data-dismiss="alert">
        <span aria-hidden="true">&times;</span><span class="sr-only">Close</span>
    </button>
      {load0}, {load1}, {load2}
    </div>
  </div>
"""

class LoadWidget(RunwayWidget):
    widget_name = "dev_server_load_widget"
    widget_label = "Server load"
    
    # js_libs = ["static/d3.js", "static/nvd3.js"]
    # css_libs = ["static/nvd3.css"]
    permissions = ["developer"]
    
    default_data = """{
        
    }"""
    
    def load(self, the_uwidget):
        """Take a JSON string from the database and create data"""
        data = json.loads(the_uwidget.data)
    
    def save(self):
        """Return a JSON string of the data for the database"""
        return json.dumps({})
    
    def form_render(self, request, the_uwidget):
        return ""
    
    def form_save(self, params):
        pass
    
    def view_render(self, request, the_uwidget):
        os_load = os.getloadavg()
        status = "info"
        
        return _view_template.format(
            load0 = round(os_load[0],2),
            load1 = round(os_load[1],2),
            load2 = round(os_load[2],2),
            status = status,
        )
