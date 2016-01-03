from ...base import DBSession
# from ...system.models.user import User

# from collections import namedtuple
from sqlalchemy.orm import aliased
from ..models import Trigger, TriggerScript
from sqlalchemy import and_, or_
# from .. import human_time
from ...system.lib import render_f
from ...system.models.user import User
from . import script_f
# from datetime import datetime

_triggers = {}
get_trigger_types = _triggers.values

_triggers_enabled = True

def register(the_trigger):
    _triggers[the_trigger.name] = the_trigger

def collect_triggers():
    for c in Trigger.__subclasses__():
        _triggers[c.name] = c

def get_trigger(trigger_name):
    return _triggers[trigger_name]

script_f.get_trigger = get_trigger

def create_instance(the_trigger):
    TheType = get_instance(the_trigger.job)
    the_instance = TheType()
    the_instance.load(the_trigger)
    return the_instance

def check_permission(the_user, owner):
    if the_user.id == owner:
        return True
    
    if owner > 2:
        if "triggers.admin" in the_user.permissions():
            return True
    else:
        if "triggers.su" in the_user.permissions():
            return True
    
    return False

def call_trigger(trigger_name, **kwargs):
    """
    This is the main call-point for triggers
    """
    if not _triggers_enabled:
        return
    
    the_trigger = get_trigger(trigger_name)
    
    results = the_trigger()(**kwargs)
    
    subscribers = get_subscribers(trigger_name, True, "owner")
    
    for the_trigger_script, the_owner in subscribers:
        script_f.execute_trigger_script(the_trigger_script, the_owner, results)
    
    # Find and fire off actions
    return results

def save(the_trigger_script, return_id=False):
    DBSession.add(the_trigger_script)
    
    if return_id:
        return DBSession.query(
            TriggerScript.id
        ).filter(
            TriggerScript.label == the_trigger_script.label
        ).order_by(
            TriggerScript.id.desc()
        ).first()[0]

def delete_trigger_script(trigger_script_id):
    DBSession.query(TriggerScript).filter(TriggerScript.id == trigger_script_id).delete()

def get_trigger_scripts(owner_id):
    return DBSession.query(TriggerScript).filter(TriggerScript.owner == owner_id).order_by(TriggerScript.label)

def get_trigger_script(trigger_script_id):
    return DBSession.query(TriggerScript).filter(TriggerScript.id == trigger_script_id).first()


def get_subscribers(trigger_name, only_active, *other_tables):
    """
    Get a list of all TriggerScripts which subscribe to this trigger.
    """
    
    fields     = [TriggerScript]
    filters    = [TriggerScript.trigger == trigger_name]
    joins      = []
    outerjoins = []
    
    if only_active:
        filters.append(TriggerScript.active == True)
        
    
    # By using a loop we take into account the order of the arguments
    for t in other_tables:
        if t == "owner":
            owner_table = aliased(User, name="owner_table")
            fields.append(owner_table)
            joins.append((owner_table, and_(owner_table.id == TriggerScript.owner)))
    
    return DBSession.query(*fields).filter(*filters).join(*joins).outerjoin(*outerjoins).order_by(TriggerScript.label)


def triggers_pre_render(request):
    display_flag = any((request.runway_settings.users['allow_triggers'] == 'True',
        'triggers' in request.user.permissions()
    ))
    
    if display_flag:
        request.render['user_links'].append(
            render_f.dropdown_menu_item("", "", "link", "Triggers", request.route_url('triggers.user.control_panel'))
        )
