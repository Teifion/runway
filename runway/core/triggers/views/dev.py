from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
from ..lib import triggers_f, actions_f
import json

import logging
log = logging.getLogger(__name__)

def home(request):
    layout      = common.render("viewer")
    message = None
    
    trigger_names = list(triggers_f._triggers.keys())
    trigger_names.sort()
    
    action_names = list(actions_f._actions.keys())
    action_names.sort()
    
    return dict(
        title       = "Developer: Triggers",
        layout      = layout,
        message     = message,
        
        triggers     = map(triggers_f.get_trigger, trigger_names),
        actions     = map(actions_f.get_action, action_names),
    )

def view_trigger(request):
    layout      = common.render("viewer")
    
    trigger_name = request.matchdict['trigger_name']
    the_trigger = triggers_f.get_trigger(trigger_name)
    subscribers = triggers_f.get_subscribers(trigger_name, "owner")
    
    return dict(
        title       = "Developer: Triggers",
        layout      = layout,
        the_trigger = the_trigger,
        subscribers = subscribers,
    )

def run_trigger(request):
    layout      = common.render("viewer")
    message = None
    results = ""
    
    trigger_name = request.matchdict['trigger_name']
    the_trigger = triggers_f.get_trigger(trigger_name)
    subscribers = triggers_f.get_subscribers(trigger_name, "owner")
    
    if "data" in request.params:
        kwargs = json.loads(request.params['data'])
        
        log.debug('Running trigger: {}'.format(trigger_name))
        raw_results = triggers_f.call_trigger(trigger_name, **kwargs)
        
        # It might be the data returns stuff like sets which JSON can't handle
        # if we can handle it though we'd like to pretty print it etc
        try:
            results = json.dumps(raw_results, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception:
            results = ",\n".join(['    "{}": {}'.format(k, v) for k, v in raw_results.items()])
            results = "{{\n{}\n}}".format(results)
        
        log.debug('Trigger has been run: {}'.format(trigger_name))
        log.debug('Results of trigger: {}'.format(results))
    
    default_data = "{\n}"
    if len(the_trigger.example_inputs) > 0:
        # Try json pretty print, if not we do something simple
        try:
            default_data = json.dumps(the_trigger.example_inputs[0].items(), sort_keys=True, indent=4, separators=(',', ': '))
        except Exception:
            default_data = ",\n".join(['    "{}": {}'.format(k, v) for k, v in the_trigger.example_inputs[0].items()])
            default_data = "{{\n{}\n}}".format(default_data)
    
    return dict(
        title       = "Developer: Triggers",
        layout      = layout,
        the_trigger = the_trigger,
        
        subscribers = subscribers,
        
        results = results,
        
        default_data = default_data,
    )

def view_action(request):
    layout      = common.render("viewer")
    
    action_name = request.matchdict['action_name']
    the_action = actions_f.get_action(action_name)
    
    return dict(
        title       = "Developer: Trigger actions",
        layout      = layout,
        the_action  = the_action,
    )

def run_action(request):
    layout      = common.render("viewer")
    message = None
    results = ""
    
    action_name = request.matchdict['action_name']
    the_action = actions_f.get_action(action_name)
    
    if "data" in request.params:
        kwargs = json.loads(request.params['data'])
        
        log.debug('Running action: {}'.format(action_name))
        raw_results = actions_f.call_action(the_action, kwargs)
        
        # It might be the data returns stuff like sets which JSON can't handle
        # if we can handle it though we'd like to pretty print it etc
        try:
            results = json.dumps(raw_results, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception:
            results = ",\n".join(['    "{}": {}'.format(k, v) for k, v in raw_results.items()])
            results = "{{\n{}\n}}".format(results)
        
        log.debug('Action has been run: {}'.format(action_name))
        log.debug('Results of action: {}'.format(results))
    
    default_data = "{\n}"
    if len(the_action.examples) > 0:
        fields = zip([i[0] for i in the_action.inputs], the_action.examples[0][0])
        
        # Try json pretty print, if not we do something simple
        try:
            default_data = json.dumps(the_action.examples[0][0], sort_keys=True, indent=4, separators=(',', ': '))
        except Exception:
            default_data = ",\n".join(['    "{}": {}'.format(k, v) for k, v in the_action.examples[0][0].items()])
            default_data = "{{\n{}\n}}".format(default_data)
    
    return dict(
        title        = "Developer: actions",
        layout       = layout,
        the_action   = the_action,
        
        results      = results,
        
        default_data = default_data,
    )
