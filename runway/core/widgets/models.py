from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    Float,
    String,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import ARRAY
from ...core.base import Base

class UserWidget(Base):
    __tablename__    = 'runway_user_widgets'
    id               = Column(Integer, primary_key=True)
    
    user             = Column(Integer, ForeignKey("runway_users.id"), nullable=False, index=True)
    widget           = Column(String, nullable=False)
    label            = Column(String, nullable=False)
    data             = Column(Text, nullable=False, default="{}")

class RunwayWidget(object):
    """
    
    """
    js_libs = []
    css_libs = []
    permissions = []
    
    # Default data for new widgets of this type
    default_data = "{}"
    
    def __init__(self):
        super(RunwayWidget, self).__init__()
    
    def load(self, the_uwidget):
        """Take a JSON string from the database and create data"""
        raise Exception("Not implemented by {} widget".format(self.widget_name))
    
    def save(self):
        """Return a JSON string of the data for the database"""
        raise Exception("Not implemented by {} widget".format(self.widget_name))
    
    def save_form(self, params):
        """Save the results of the form"""
        raise Exception("Not implemented by {} widget".format(self.widget_name))
    
    def form_render(self, request, the_uwidget):
        """Used to render a form for editing details"""
        raise Exception("Not implemented by {} widget".format(self.widget_name))
    
    def view_render(self, request, the_uwidget):
        """Used to render a view"""
        raise Exception("Not implemented by {} widget".format(self.widget_name))


class JSWidget(object):
    """
    A javascript widget.
    
    All it does is to inject JS and CSS into a web page using the render_tween
    methods of adding in libs and raws.
    
    Init with a call to the request. e.g.
    
    JSWidget(requset)
    
    It is really that simple.
    """
    js_libs = ()
    css_libs = ()
    
    raw_js = ()
    raw_css = ()
    raw_html = ()
    
    def __init__(self, request):
        super(JSWidget, self).__init__()
        
        for j in self.js_libs:
            request.add_js_lib(j)
        
        for c in self.css_libs:
            request.add_css_lib(c)
        
        if isinstance(self.raw_js, str):
            request.add_js_raw(self.raw_js)
        else:
            for j in self.raw_js:
                request.add_js_raw(j)
        
        if isinstance(self.raw_css, str):
            request.add_css_raw(self.raw_css)
        else:
            for c in self.raw_css:
                request.add_css_raw(c)
        
        if isinstance(self.raw_html, str):
            request.add_html_raw(self.raw_html)
        else:
            for h in self.raw_html:
                request.add_html_raw(h)
