from ...base import DBSession
from ...system.models.user import User

from collections import namedtuple
from ..models import UserWidget, RunwayWidget

_widgets = {}
get_rtypes = _widgets.values

def register(the_widget):
    _widgets[the_widget.name] = the_widget

def collect_widgets():
    for c in RunwayWidget.__subclasses__():
        _widgets[c.widget_name] = c

def get_rwidget_type(widget_name):
    return _widgets[widget_name]

def get_rwidget(the_uwidget):
    TheType = get_rwidget_type(the_uwidget.widget)
    the_rwidget = TheType()
    the_rwidget.load(the_uwidget)
    return the_rwidget
    

def get_uwidget(widget_id):
    return DBSession.query(UserWidget).filter(UserWidget.id == widget_id).first()

def get_uwidgets(user_id):
    return DBSession.query(UserWidget).filter(UserWidget.user == user_id)

def delete_uwidget(widget_id):
    DBSession.query(UserWidget).filter(UserWidget.id == widget_id).delete()

def save(the_uwidget, the_rwidget=None, return_id=False):
    if the_rwidget != None:
        the_uwidget.data = the_rwidget.save()
    
    DBSession.add(the_uwidget)
    
    if return_id:
        return DBSession.query(UserWidget.id).filter(UserWidget.label == the_uwidget.label).order_by(UserWidget.id.desc()).first()[0]
