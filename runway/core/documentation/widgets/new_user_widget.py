from ....core.widgets.models import RunwayWidget
from ....core.lib import common
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
    
    <div class="row">
      <dic class="col-lg-4 col-md-6">
        
        <div class="panel panel-default">
          <div class="panel-heading">
            <i class="fa fa-user fa-fw"></i>
            {site_name}
          </div>
          
          <div class="panel-body">
            <i class="fa fa-user fa-fw fa-2x"></i>
            <i class="fa fa-book fa-fw fa-2x"></i>
            <br />
            <p>Along the side of the page are links to different sections and modules in the system. When you're in a section, the relevant sidebar icon will be highlighted.</p>
            
            <p>Along the top there will be icons such as the person and book as shown above this text. The icon of a person is the user control panel. It allows you to change your password and personal settings. The book icon appears on any page with related documentation, it contains said related documentation.</p>
            
          </div>
        </div>
        
      </div>
    </div>
    
  </div>
"""

class NewUserWidget(RunwayWidget):
    widget_name = "documentation_new_user"
    widget_label = "New user information"
    
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
        return _view_template.format(
            site_name = request.runway_settings.system['name'],
        )
