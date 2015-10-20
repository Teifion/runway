from ....core.widgets.models import JSWidget

class ExampleJSWidget(JSWidget):
    js_libs  = ()
    css_libs = ()
    
    raw_js = ("""
    $(function() {
      alert("You are using the Example JS Widget");
    });
    """)
    raw_css = ()
