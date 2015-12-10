from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
from ..lib import triggers_f, actions_f, script_f
from ..models import TriggerScript
import json

def control_panel(request):
    layout      = common.render("viewer")
    message = None
    
    user_trigger_scripts = triggers_f.get_trigger_scripts(request.user.id)
    
    return dict(
        title                = "User control panel",
        layout               = layout,
        pre_content          = pre_content,
        message              = message,
        
        user_trigger_scripts = user_trigger_scripts,
        
        trigger_types        = {t.name:t.label for t in triggers_f.get_trigger_types()},
    )

def create(request):
    layout      = common.render("viewer")
    message = None
    
    if "trigger_label" in request.params and "trigger_type" in request.params:
        t = TriggerScript(
            owner      = request.user.id,
            trigger    = request.params['trigger_type'],
            label      = request.params['trigger_label'],
            actions    = '{"actions":[], "conditions":[]}',
            comments   = "",
            active     = False,
            valid_code = True,
        )
        trigger_script_id = triggers_f.save(t, return_id=True)
        return HTTPFound(request.route_url('triggers.user.edit', trigger_script_id=trigger_script_id))
    
    def _test_permissions(trigger_type):
        for p in trigger_type.permissions:
            if p not in request.user.permissions():
                return False
        return True
    
    trigger_types = {t.name:t.label for t in filter(_test_permissions, triggers_f.get_trigger_types())}
    
    return dict(
        title       = "Create new trigger",
        layout      = layout,
        message     = message,
        
        trigger_type_select = common.select_box("trigger_type", trigger_types),
    )

def edit(request):
    layout      = common.render("viewer")
    message = None
    validity = None
    
    the_trigger_script = triggers_f.get_trigger_script(int(request.matchdict['trigger_script_id']))
    
    if not triggers_f.check_permission(request.user, the_trigger_script.owner):
        return HTTPFound(request.route_url('triggers.user.control_panel'))
    
    if "trigger_label" in request.params:
        the_trigger_script.label = request.params['trigger_label']
        the_trigger_script.comments = request.params['comments']
        the_trigger_script.active = "active" in request.params
        
        triggers_f.save(the_trigger_script)
        
        message = "success", "Changes saved"
    
    elif "trigger_code" in request.params:
        the_trigger_script.actions = request.params['trigger_code']
        
        # If it's active we want to check to see if it's valid
        try:
            validity, highlights = script_f.validate(the_trigger_script)
            parse_errors = False
        except Exception as e:
            # raise
            validity = [e.args[0]]
            highlights = {}
            parse_errors = True
        
        the_trigger_script.valid_code = True if validity == [] else False
        triggers_f.save(the_trigger_script)
        
    
    # No need to do this twice!
    if validity is None:
        try:
            validity, highlights = script_f.validate(the_trigger_script)
            parse_errors = False
        except Exception as e:
            # raise
            validity = [e.args[0]]
            highlights = {}
            parse_errors = True
    
    json_error = None
    try:
        script_data = json.loads(the_trigger_script.actions)
        json_value_tree = script_f.build_value_tree(the_trigger_script)
        pretty_printed_source = json.dumps(script_data, sort_keys=True, indent=4, separators=(',', ': '))
    except Exception as e:
        json_error = e.args[0]
        
        script_data = {"actions":[], "conditions":[]}
        json_value_tree = ""
        pretty_printed_source = the_trigger_script.actions
    
    return dict(
        title                 = "Edit trigger",
        layout                = layout,
        pre_content           = pre_content,
        message               = message,
        
        json_value_tree       = json_value_tree,
        pretty_printed_source = pretty_printed_source,
        
        parse_errors          = parse_errors,
        validity              = validity,
        
        the_trigger_script    = the_trigger_script,
        the_trigger           = triggers_f.get_trigger(the_trigger_script.trigger),
        
        json_error            = json_error,
    )

def gui_edit(request):
    layout      = common.render("viewer")
    message = None
    validity = None
    
    the_trigger_script = triggers_f.get_trigger_script(int(request.matchdict['trigger_script_id']))
    
    if not triggers_f.check_permission(request.user, the_trigger_script.owner):
        return HTTPFound(request.route_url('triggers.user.control_panel'))
    
    mode = request.params.get("mode", "")
    
    def _get_action(script_data, action_name):
        for i, a in enumerate(script_data['actions']):
            if a['name'] == action_name:
                return i
    
    if mode == "":
        pass
    
    elif mode == "action_type":
        action_name = request.params['action_name']
        new_type = request.params['action_type']
        
        # Find the action we're working on
        script_data = json.loads(the_trigger_script.actions)
        action_index = _get_action(script_data, action_name)
        the_action = script_data['actions'][action_index]
        
        # No changes to be made?
        if new_type == the_action['action']:
            return HTTPFound(request.route_url('triggers.user.gui_edit', trigger_script_id=the_trigger_script.id))
        
        # Do stuff
        the_action['action'] = new_type
        
        new_input_map = {}
        for data_name, data_type, _ in actions_f.get_action(new_type).inputs:
            new_input_map[data_name] = the_action['input_map'].get(data_name, None)
        
        the_action['input_map'] = new_input_map
        
        # Find new name
        i, found = 0, True
        while found:
            i += 1
            found = False
            proposed_name = "{}_{}".format(new_type, i)
            for a in script_data['actions']:
                if a['name'] == proposed_name:
                    found = True
        
        the_action['name'] = proposed_name
        
        
        # Re-save
        script_data['actions'][action_index] = the_action
        
        the_trigger_script.actions = json.dumps(script_data)
        
        try:
            validity = script_f.validate(the_trigger_script)[0]
        except Exception as e:
            validity = [e.args[0]]
        the_trigger_script.valid_code = True if validity == [] else False
        
        triggers_f.save(the_trigger_script)
        
        return HTTPFound(request.route_url('triggers.user.gui_edit', trigger_script_id=the_trigger_script.id))
    
    elif mode == "delete_action":
        action_name = request.params['action_name']
        
        # Find the action we're working on
        script_data = json.loads(the_trigger_script.actions)
        action_index = _get_action(script_data, action_name)
        
        # Remove this action
        del(script_data['actions'][action_index])
        
        # Re-save
        the_trigger_script.actions = json.dumps(script_data)
        
        try:
            validity = script_f.validate(the_trigger_script)[0]
        except Exception as e:
            validity = [e.args[0]]
        the_trigger_script.valid_code = True if validity == [] else False
        
        triggers_f.save(the_trigger_script)
        
        return HTTPFound(request.route_url('triggers.user.gui_edit', trigger_script_id=the_trigger_script.id))
        
        
    elif mode == "edit_action":
        # Find the action we're working on
        action_name = request.params['action_name']
        script_data = json.loads(the_trigger_script.actions)
        action_index = _get_action(script_data, action_name)
        the_action = script_data['actions'][action_index]
        
        # Do stuff
        new_input_map = {}
        for data_name, data_type, _ in actions_f.get_action(the_action['action']).inputs:
            if data_name in ("args", "kwargs"): continue
            
            raw_data = request.params.get("{}_raw".format(data_name), "")
            selected_data = request.params.get(data_name, "")
            
            if selected_data == " hardcoded":
                converted_data = script_f.convert(raw_data, data_type)
                
                if isinstance(converted_data, list):
                    converted_data = [c.replace('"', '\\"') for c in converted_data]
                else:
                    converted_data = '"{}"'.format(converted_data.replace('"', '\\"'))
                
                new_input_map[data_name] = converted_data
            else:
                new_input_map[data_name] = selected_data
        
        # Same as with args but kwargs instead
        if 'kwargs' in (i[0] for i in actions_f.get_action(the_action['action']).inputs):
            kwargs = {}
            i = -1
            loop_flag = True
            
            while loop_flag:
                i += 1
                if 'kwarg_{}_key'.format(i) not in request.params:
                    loop_flag = False
                    continue
                
                key = request.params['kwarg_{}_key'.format(i)]
                value = request.params['kwarg_{}_value'.format(i)]
                raw = request.params['kwarg_{}_raw'.format(i)]
                
                if value == " hardcoded":
                    kwargs[key] = '"{}"'.format(raw.replace('"', '\\"'))
                else:
                    kwargs[key] = value
            
            new_input_map['kwargs'] = kwargs
        
        
        the_action['label'] = request.params['label']
        the_action['input_map'] = new_input_map
        
        # Re-save
        script_data['actions'][action_index] = the_action
        
        the_trigger_script.actions = json.dumps(script_data)
        
        try:
            validity = script_f.validate(the_trigger_script)[0]
        except Exception as e:
            validity = [e.args[0]]
        the_trigger_script.valid_code = True if validity == [] else False
        
        triggers_f.save(the_trigger_script)
        
        return HTTPFound(request.route_url('triggers.user.gui_edit', trigger_script_id=the_trigger_script.id))
    
    elif mode == "add_action":
        action_type = request.params['action_type']
        action_label = request.params['new_action_label']
        
        script_data = json.loads(the_trigger_script.actions)
        i, found = 0, True
        while found:
            i += 1
            found = False
            proposed_name = "{}_{}".format(action_type, i)
            for a in script_data['actions']:
                if a['name'] == proposed_name:
                    found = True
        
        script_data['actions'].append({
            "name": proposed_name,
            "label": action_label,
            "action": action_type,
            "input_map": {}
        })
        
        the_trigger_script.actions = json.dumps(script_data)
        
        triggers_f.save(the_trigger_script)
        
        return HTTPFound(request.route_url('triggers.user.gui_edit', trigger_script_id=the_trigger_script.id))
    
    
    elif mode == "add_condition":
        source = request.params['source']
        operator = request.params['operator']
        value = request.params['value']
        
        new_condition = [source, operator, value]
        
        script_data = json.loads(the_trigger_script.actions)
        script_data['conditions'].append(new_condition)
        
        if isinstance(script_data['conditions'][0], list):
            script_data['conditions'].insert(0, "and")
        
        the_trigger_script.actions = json.dumps(script_data)
        
        triggers_f.save(the_trigger_script)
        
        return HTTPFound(request.route_url('triggers.user.gui_edit', trigger_script_id=the_trigger_script.id))
        
    elif mode == "edit_conditions":
        script_data = json.loads(the_trigger_script.actions)
        
        conditions = []
        i = -1
        loop_flag = True
        
        while loop_flag:
            i += 1
            if 'source_{}'.format(i) not in request.params:
                loop_flag = False
                continue
            
            source = request.params['source_{}'.format(i)]
            operator = request.params['operator_{}'.format(i)]
            value = request.params['value_{}'.format(i)]
            
            conditions.append([source, operator, value])
        
        script_data['conditions'] = ["and"] + conditions
        the_trigger_script.actions = json.dumps(script_data)
        
        triggers_f.save(the_trigger_script)
        
        return HTTPFound(request.route_url('triggers.user.gui_edit', trigger_script_id=the_trigger_script.id))
    
    elif mode == "cardinality_up":
        action_name = request.params['action']
        
        # Find the action we're working on
        script_data = json.loads(the_trigger_script.actions)
        action_index = _get_action(script_data, action_name)
        
        script_data['actions'][action_index], script_data['actions'][action_index-1] = script_data['actions'][action_index-1], script_data['actions'][action_index]
        
        # Re-save
        the_trigger_script.actions = json.dumps(script_data)
        
        # try:
        #     validity = script_f.validate(the_trigger_script)[0]
        # except Exception as e:
        #     validity = [e.args[0]]
        # the_trigger_script.valid_code = True if validity == [] else False
        
        triggers_f.save(the_trigger_script)
        
        return HTTPFound(request.route_url('triggers.user.gui_edit', trigger_script_id=the_trigger_script.id))
        
    elif mode == "cardinality_down":
        action_name = request.params['action']
        
        # Find the action we're working on
        script_data = json.loads(the_trigger_script.actions)
        action_index = _get_action(script_data, action_name)
        
        script_data['actions'][action_index], script_data['actions'][action_index+1] = script_data['actions'][action_index+1], script_data['actions'][action_index]
        
        # Re-save
        the_trigger_script.actions = json.dumps(script_data)
        
        # try:
        #     validity = script_f.validate(the_trigger_script)[0]
        # except Exception as e:
        #     validity = [e.args[0]]
        # the_trigger_script.valid_code = True if validity == [] else False
        
        triggers_f.save(the_trigger_script)
        
        return HTTPFound(request.route_url('triggers.user.gui_edit', trigger_script_id=the_trigger_script.id))
        
    else:
        raise Exception("Not implemented mode of '{}'".format(mode))
    
    def _test_permissions(trigger_type):
        for p in trigger_type.permissions:
            if p not in request.user.permissions():
                return False
        return True
    
    try:
        validity, highlights = script_f.validate(the_trigger_script)
        parse_errors = False
    except Exception as e:
        # raise
        validity = [e.args[0]]
        highlights = {}
        parse_errors = True
    
    
    trigger_types = {t.name:"{}: {}".format(t.group, t.label) for t in filter(_test_permissions, triggers_f.get_trigger_types())}
    action_types = {a.name:"{}: {}".format(a.group, a.label) for a in filter(_test_permissions, actions_f.get_action_types())}
    
    script_data = json.loads(the_trigger_script.actions)
    
    json_error = None
    try:
        json_value_tree = script_f.build_value_tree(the_trigger_script)
    except Exception as e:
        json_error = e.args[0]
        json_value_tree = ""
    
    condition_list = [(i,a,b,c) for (i, (a,b,c)) in enumerate(script_data['conditions'][1:])]
    action_list = script_data['actions']
    
    sources = [
        " hardcoded",
        "owner.id",
        "owner.username",
        "owner.display_name",
        "owner.email",
        "owner.join_date"
    ]
    for o, _, _ in triggers_f.get_trigger(the_trigger_script.trigger).outputs:
        sources.append("trigger.{}".format(o))
    
    for a in script_data['actions']:
        atype = actions_f.get_action(a['action'])
        for o in atype.outputs:
            sources.append("{}.{}".format(a['name'], o[0]))
        
    
    source_selector = lambda name, sel: common.select_box(name, sources, selected=sel, custom_id=None)
    condition_source_selector = lambda name, sel: common.select_box(name, sources[1:], selected=sel, custom_id=None)
    operator_selector = lambda name, sel: common.select_box(name, list(script_f._ops.keys()), selected=sel, custom_id=None)
    action_selector = lambda ci, sel: common.select_box("action_type", action_types, selected=sel, custom_id=ci)
    
    return dict(
        title              = "Edit trigger actions",
        layout             = layout,
        pre_content        = pre_content,
        message            = message,
        
        the_trigger_script = the_trigger_script,
        
        source_selector    = source_selector,
        json_value_tree    = json_value_tree,
        
        validity           = validity,
        
        condition_list     = condition_list,
        action_list        = action_list,
        get_action         = actions_f.get_action,
        
        action_selector    = action_selector,
        operator_selector = operator_selector,
        condition_source_selector = condition_source_selector,
        
        json_error         = json_error,
        
        highlights    = highlights,
    )

def delete(request):
    layout      = common.render("viewer")
    message = None
    
    trigger_script_id = int(request.matchdict['trigger_script_id'])
    the_trigger_script = triggers_f.get_trigger_script(int(request.matchdict['trigger_script_id']))
    
    if not triggers_f.check_permission(request.user, the_trigger_script.owner):
        return HTTPFound(request.route_url('triggers.user.control_panel'))
    
    if int(request.params.get('confirm', '-1')) == trigger_script_id:
        triggers_f.delete_trigger_script(trigger_script_id)
        return HTTPFound(request.route_url('triggers.user.control_panel'))
    
    return dict(
        title             = "Remove trigger",
        layout            = layout,
        pre_content       = pre_content,
        message           = message,
        
        trigger_script_id = trigger_script_id,
    )

def test_trigger_script(request):
    layout      = common.render("viewer")
    message = None
    
    trigger_script_id = int(request.matchdict['trigger_script_id'])
    the_trigger_script = triggers_f.get_trigger_script(int(request.matchdict['trigger_script_id']))
    
    results = script_f.dry_run(the_trigger_script, the_owner=request.user)
    
    return dict(
        title             = "Test Trigger Script",
        layout            = layout,
        pre_content       = pre_content,
        message           = message,
        
        results           = json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '), default=common.json_default),
        trigger_script_id = trigger_script_id,
    )