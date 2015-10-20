# from ...base import DBSession
# from ...system.models.user import User

# from collections import namedtuple
from ..models import Action
# from sqlalchemy import and_, or_
# from .. import human_time
# from ...system.lib import errors_f
# from ...system.models.user import User
# from datetime import datetime
from . import script_f

# import sys
# import transaction

_actions = {}
get_action_types = _actions.values

def register(the_action):
    _actions[the_action.name] = the_action

def collect_actions():
    for c in Action.__subclasses__():
        _actions[c.name] = c

def get_action(action_name):
    return _actions[action_name]
script_f.get_action = get_action

def create_instance(the_action):
    TheType = get_instance(the_action.job)
    the_instance = TheType()
    the_instance.load(the_action)
    return the_instance

def call_action(the_action, raw_kwargs):
    """
    This allows us to use varadic parameters when calling actions (*args and **kwargs)
    """
    kwargs = {}
    args = []
    
    if "args" in raw_kwargs:
        args = raw_kwargs['args']
        del(raw_kwargs['args'])
    
    if "kwargs" in raw_kwargs:
        kwargs = raw_kwargs['kwargs']
        del(raw_kwargs['kwargs'])
    
    kwargs.update(raw_kwargs)
    
    return the_action()(*args, **kwargs)