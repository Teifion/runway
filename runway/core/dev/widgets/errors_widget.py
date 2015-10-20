from ....core.widgets.models import RunwayWidget
from ....core.lib import common
from ..lib import exceptions_f
import json

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
      There are currently <a href="{url}" class="alert-link">{count} exception{plural}</a>
    </div>
  </div>
"""

_periods = {
    "month to date": "Month to date",
    "last month": "Last month",
    "year to date": "Year to date",
}

class ErrorsWidget(RunwayWidget):
    widget_name = "dev_errors_widget"
    widget_label = "Exception count"
    
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
        assigned_count = exceptions_f.exception_count(request.user.id).get(request.user.id,0)
        unassigned_count = exceptions_f.exception_count(request.user.id).get(None,0)
        
        count = assigned_count + unassigned_count
        
        if count < 1:
            status = "success"
        elif count < 3:
            status = "warning"
        else:
            status = "danger"
        
        return _view_template.format(
            plural = "" if count == 1 else "s",
            count = count,
            status = status,
            url = request.route_url('dev.exception.list'),
        )
