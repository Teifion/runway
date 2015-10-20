from ....core.widgets.models import RunwayWidget
from ....core.lib import common
import json
import os

_form_template = """
  <div class="form-group">
    <label for="time_period" class="col-sm-2 control-label">Message:</label>
    <div class="col-sm-10">
      <input type="text" name="message" id="message" value="{message}" placeholder="Hello world" class="form-control" />
    </div>
  </div>
"""

_view_template = """
  <div>
    <div class="alert alert-info alert-dismissible" role="alert">
      <button type="button" class="close" data-dismiss="alert">
        <span aria-hidden="true">&times;</span><span class="sr-only">Close</span>
      </button>
      {message}
    </div>
  </div>
"""

class ExampleWidget(RunwayWidget):
    widget_name = "widgets_example_widget"
    widget_label = "Example widget"
    
    js_libs = []
    css_libs = []
    
    default_data = """{
        "message": "Hello world"
    }"""
    
    def load(self, the_uwidget):
        """Take a JSON string from the database and create data"""
        data = json.loads(the_uwidget.data)
        
        self.message = data['message']
    
    def save(self):
        """Return a JSON string of the data for the database"""
        return json.dumps({
            'message': self.message,
        })
    
    def form_render(self, request, the_uwidget):
        return _form_template.format(
            message = self.message
        )
    
    def form_save(self, params):
        self.message = params.get('message', 'Hello world')
    
    def view_render(self, request, the_uwidget):
        return _view_template.format(
            message = self.message,
        )

