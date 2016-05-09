from datetime import date, datetime, timedelta
from ...system.lib import user_f

import json
import logging

log = logging.getLogger(__name__)

"""
get_trigger() and get_action() are defined in triggers_f and actions_f
but then assigned to the variable here to prevent circular imports
"""
get_trigger = None
get_action = None

"""
Operators we may want to use in our conditionals
"""
_ops = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
    "in": lambda a, b: a in b,
}

"""
Functions for those who like to use the code view
"""
_funcs = {
    "len": lambda a: len(a),
}

def _get_val(data, term):
    """
    term refers to a string such as "double len trigger.count" and will
    find the functions "double" and "len" and apply them to "triger.count"
    essentially it evalulates the value itself ready to be passed into
    the operator.
    """
    
    # Not a string? Just send the term back as it is, it's
    # apparently a raw value
    if not isinstance(term, str):
        return term
    
    if term[0] == '"' and term[-1] == '"':
        return term[1:-1]
    
    # Get funcs
    funcs = []
    if " " in term:
        funcs = term.split(" ")[:-1]
        term = term.split(" ")[-1]
    
    # Get value
    if "." in term:
        key, attr = term.split(".")
        value = data[key][attr]
    else:
        value = term
    
    if len(funcs) > 0:
        for f in (_funcs[fname] for fname in funcs[::-1]):
            value = f(value)
    
    # Apply funcs
    return value

def _find_condition_names(parts):
    """
    Pre-scans the condition tree and brings back all the names, thus
    we can use it to calculate which actions we HAVE to calculate to
    check the conditions. This probably won't be needed for a while
    but it may allow for some very cool meta-programming options 
    for more advanced users (or possibly some macros of some sort?)
    """
    names = set()
    
    for p in parts:
        if isinstance(p, str):
            if "." in p:
                names.add(p.split(" ")[-1].split(".")[0])
        elif isinstance(p, list):
            names.update(_find_condition_names(p))
    
    return names

def _perform_action(action_dict, data, test_mode=True):
    the_action = get_action(action_dict['action'])
    
    # If there's kwargs in the dict, flatten it all
    input_dict = dict(action_dict['input_map'])
    if "**kwargs" in input_dict:
        input_dict.update(input_dict['**kwargs'])
        del(input_dict['**kwargs'])
    
    args = []
    if "*args" in input_dict:
        for v in input_dict['*args']:
            if v[0] == '"':
                # Hard coded value, strip off the quote marks for the value
                calculated_value = v[1:-1]
            else:
                
                # Try to grab it!
                try:
                    calculated_value = _get_val(data, v)
                except Exception:
                    raise Exception("Error getting the value '{}' (found in {})".format(v, action_dict['name']))
        
        del(input_dict['*args'])
    
    kwargs = {}
    for k, v in input_dict.items():
        if k == "args": continue
        
        if isinstance(v, list):
            calculated_value = [_get_val(data, item) for item in v]
            kwargs[k] = calculated_value
        
        elif isinstance(v, dict):
            calculated_value = {}
            for key, item in v.items():
                kwargs[key] = _get_val(data, item)
            
        else:
            if v[0] == '"':
                # Hard coded value, strip off the quote marks for the value
                calculated_value = v[1:-1]
            else:
                
                # Try to grab it!
                try:
                    calculated_value = _get_val(data, v)
                except Exception:
                    raise Exception("Error getting the value '{}' (found in {})".format(v, action_dict['name']))
            
            kwargs[k] = calculated_value
    
    # Set test mode
    kwargs['test_mode'] = test_mode
    
    try:
        return the_action()(*args, **kwargs)
    except Exception as e:
        raise
        raise Exception("Error running action {} ({}): Exception of {}".format(
            action_dict['label'],
            action_dict['name'],
            e.args[0],
        ))
    

def make_eval(data):
    """
    Main evaluation function for the conditions, retuns the evaluator function. Loops through
    each list, if the first item is a condition it recursively calls itself
    based on that condition.
    
    When presented with a condition itself it breaks it into value A, value B and
    the operator. It calculates values A and B and then applys the operator
    condition, returning the result of said operator.
    """
    
    def f(part):
        if part == []: return False
        
        if part[0] == "and":
            return all(map(f, part[1:]))
        if part[0] == "or":
            return any(map(f, part[1:]))
        
        a, op, b = part
        
        a = _get_val(data, a)
        b = _get_val(data, b)
        
        result = _ops[op](a, b)
        
        log.debug("Eval: %s (%s, %s) -> %s", part, a, b, result)
        return result
    
    return f

def validate(the_trigger_script):
    """
    If it's a parse/structure issue then issue an exception. If it's
    a data validation (bad naming etc) then send back a reason.
    """
    
    results = []
    highlights = {}
    
    # First, can we actually load the data?
    try:
        script_data = json.loads(the_trigger_script.actions)
    except Exception as e:
        raise Exception("Parse error: Failed to load JSON data ({})".format(e.args[0]))
    
    # Check actions data
    if 'actions' not in script_data:
        raise Exception("Parse error: No actions key present in data")
    
    if not isinstance(script_data['actions'], list):
        raise Exception("Parse error: data['actions'] is not of type List")
    
    action_names = [a.get('name', None) for a in script_data['actions']]
    if len(action_names) != len(set(action_names)):
        raise Exception("Parse error: One or more action names are duplicated")
    
    # Check conditions data
    if 'conditions' not in script_data:
        raise Exception("Parse error: No conditions present in data")
    
    if not isinstance(script_data['conditions'], list):
        raise Exception("Parse error: data['conditions'] is not of type List")
    
    # Now check we can find names
    try:
        names = _find_condition_names(script_data['conditions'])
    except Exception as e:
        raise Exception("Parse error: Exception trying to find names in script data ({})".format(e.args[0]))
    
    # Now we check to ensure all those names actually exist
    valid_names = set(action_names) | {'trigger', 'owner'}
    for n in names:
        if n not in valid_names:
            results.append("Validation error: Could not find the name '{}' (referenced in triggers)".format(n))
    
    # Now we want to make sure all the inputs and outputs line up
    the_trigger = get_trigger(the_trigger_script.trigger)
    
    # Allows us to easily map output types for validation
    def _map_outputs(obj):
        return {name:out_type for name, out_type, _ in obj.outputs}
    
    action_lookup = {
        "trigger":_map_outputs(the_trigger),
        "owner": {
            "id": int,
            "username": str,
            "display_name": str,
            "email": str,
            "join_date": date,
        }
    }
    
    def _find_type(term, *allowed):
        """Allows us to ensure a given output is of the correct type"""
        
        if not isinstance(term, str):
            return type(term)
        
        if term[0] == '"':
            the_type = str
        
        else:
            # First lets break it down to the parts
            funcs = []
            if " " in term:
                funcs = term.split(" ")[:-1]
                term = term.split(" ")[-1]
            
            # TODO
            # At this stage we should take the return type of the first function
            # however I've not thought of a nice way to do this
        
            # Get value
            key, attr = term.split(".")
            the_type = action_lookup[key][attr]
        
        return the_type
    
    
    for a in script_data['actions']:
        try:
            the_action = get_action(a['action'])
            action_lookup[a['name']] = _map_outputs(the_action)
        except Exception:
            results.append("Validation error: No action of type '{}'".format(a['action']))
            continue
        
        expected_inputs = [i[0] for i in the_action.inputs]
        
        # Ensure every expected action is present
        for iname, itype, _ in the_action.inputs:
            if iname in ('kwargs', 'args'):
                continue
            
            try:
                script_input = a['input_map'][iname]
            except KeyError:
                highlights["action.{}".format(a['name'])] = ""
                results.append("Validation error: No map for action input '{}.{}'".format(a['name'], iname))
                highlights["source.{}.{}".format(a['name'], iname)] = "There's no input value for this field, without it the action can't run."
            
            if _find_type(script_input) != itype:
                highlights["source.{}.{}".format(a['name'], iname)] = "This input is expecting a type of {expected_type} yet is being given a type of {actual_type}. You will need to change the type so they match. You can see the types created by various actions on the values table (there is a button at the top of the window)".format(
                        expected_type = itype.__name__,
                        actual_type   = _find_type(script_input).__name__,
                )
                highlights["action.{}".format(a['name'])] = ""
                
                results.append("""Type error: The input for {input_label}: {input_action}.{input_field} expects a type of "{expected_type}" but instead it's being sent a "{actual_type}" (source {source_value})""".format(
                        input_label   = a['label'],
                        input_action  = a['name'],
                        input_field   = iname,
                        expected_type = itype.__name__,
                        actual_type   = _find_type(script_input).__name__,
                        source_value  = script_input,
                ))
        
        # Now ensure we've not got any extra names
        if 'kwargs' not in expected_inputs:
            for iname in a['input_map']:
                if iname not in expected_inputs:
                    results.append("Validation warning: Extra input '{}' for '{}'".format(iname, a['name']))
    
    try:
        dry_run(the_trigger_script)
    except Exception as e:
        # raise
        results.append("Dry run error: {}".format(e.args[0]))
    
    return results, highlights

def dry_run(the_trigger_script, the_owner=None):
    results = []
    
    if the_owner is None:
        the_owner = user_f.get_user(the_trigger_script.owner)
    
    script_data = json.loads(the_trigger_script.actions)
    data = {'owner':dict(the_owner.__dict__)}
    
    # This information should never go through a trigger script
    del(data['owner']['password'])
    del(data['owner']['secure_password'])
    del(data['owner']['_sa_instance_state'])
    del(data['owner']['_permissions'])
    
    # Add trigger data
    the_trigger = get_trigger(the_trigger_script.trigger)
    data['trigger'] = the_trigger.example_inputs[0]
    
    # Find out which (if any) actions we need to evaluate for the conditional
    names = _find_condition_names(script_data['conditions'])
    found_names = {'trigger', 'owner'}
    
    # Get a list of just the names we've not found
    names = {n for n in names if n not in found_names}
    
    # If we're using the output of an action as a condition then
    # names will have a length greater than 1 and
    # we will need to evaluate some actions regardless
    for a in script_data['actions']:
        if len(names) == 0: continue
        
        data[a['name']] = _perform_action(a, data, test_mode=True)
        names.remove(a['name'])
    
    """
    At this stage we've met the requirements of the conditionals
    lets try evaluating it, we don't actually care if it's
    legit or not, we're testing to see if it runs (we don't know
    if it's correct or not)
    """
    make_eval(data)(script_data['conditions'])
    
    for a in script_data['actions']:
        if a['name'] in data: continue
        
        data[a['name']] = _perform_action(a, data, test_mode=True)
    
    return data


def execute_trigger_script(the_trigger_script, the_owner, trigger_data):
    script_data = json.loads(the_trigger_script.actions)
    data = {'owner':dict(the_owner.__dict__)}
    
    # This information should never go through a trigger script
    del(data['owner']['password'])
    del(data['owner']['secure_password'])
    del(data['owner']['_sa_instance_state'])
    del(data['owner']['_permissions'])
    
    # Add trigger data
    the_trigger = get_trigger(the_trigger_script.trigger)
    data['trigger'] = trigger_data
    
    # Find out which (if any) actions we need to evaluate for the conditional
    names = _find_condition_names(script_data['conditions'])
    found_names = {'trigger', 'owner'}
    
    # Get a list of just the names we've not found
    names = {n for n in names if n not in found_names}
    
    # If we're using the output of an action as a condition then
    # names will have a length greater than 1 and
    # we will need to evaluate some actions regardless
    for a in script_data['actions']:
        if len(names) == 0: continue
        
        data[a['name']] = _perform_action(a, data, test_mode=False)
        names.remove(a['name'])
    
    # Do we actually run the trigger?
    if script_data['conditions'] != []:
        conditions_met = make_eval(data)(script_data['conditions'])
    else:
        conditions_met = True
    
    if not conditions_met:
        return False
    
    for a in script_data['actions']:
        if a['name'] in data: continue
        
        data[a['name']] = _perform_action(a, data, test_mode=False)
    
    return True

# e = make_eval({
#     "trigger": {
#         "id": 2,
#         "username": "bob",
#     },
#     "system_formatter_1": {
#         "id": 1,
#     }
# })

# r = e([
#     "and",
#         ["trigger.id", "!=", 1],
#         ["or",
#             ["system_formatter_1.id", "!=", 1],
#             ["len trigger.username", ">", 0]
#         ]
#     ]
# )

# print("\nResult:")
# print(r)
# print("")


"""
Example code structure for an example TriggerScript based around adding a new user

Trigger: id, username, actual_name, creation_date, email, created_by
Action (Formatter): Formats the first 3 arguments into a string
Action (Email): Emails a mailing list information about the user
Action (Email): Emails the user a welcome message
"""

trigger_script_data = {
    "conditions": [
        "and",
            ["trigger.field1", "!=", 1],
            ["or",
                ["len system_formatter_1.formatted_string", ">", 1],
                ["trigger.field1", "!=", 0]
            ]
    ],
    "actions": [
        {
            "name": "system_formatter_1",
            "label": "Mailing list formatter",
            "action": "system_formatter",
            "input_map": {
                "unformatted_string": "\"A new user by the name of {actual_name} has been added with the username {username} and ID: #{id}\"",
                "kwargs": {
                    "actual_name": "trigger.field1",
                    "username": "trigger.field2",
                    "id": "trigger.field3"
                }
            }
        },
        {
            "name": "system_email_1",
            "label": "Mailing list email",
            "action": "system_email",
            "input_map": {
                "recipients": ["\"admin@localhost\"", "\"mailing_list@localhost\""],
                "content": "system_formatter_1.formatted_string",
                "subject": "\"New user\""
            }
        },
        {
            "name": "system_email_2",
            "label": "Welcome email",
            "action": "system_email",
            "input_map": {
                "recipients": ["trigger.field3"],
                "content": "\"Welcome to the site!\"",
                "subject": "\"Welcome to Runway\""
            }
        }
    ]
}



"""
Notes:
input_map -> **kwargs uses a dictionary and is handled specially. A *args
    field would get similar treatment but using a list. Normally if there were
    extra fields they would be stored the same was as unformatted_string is, with
    a 2 length list holding the source location and source field

name is always generated by the system based on the action name, it is not
    seen or edited by the user and is thus reliable in terms of uniqueness and style

"""

# def _type_str(the_type):
#     """
#     Sometimes we use entire objects to represent pointers (e.g. core.system.User)
#     while only actually passing the ID value. At the same time we don't want that
#     ID to be treated like an integer or used as the ID value for a different
#     object (e.g. core.cron.CronJob).
    
#     This function allows us to print out a bit of extra info around the name
#     for display purposes and make it more obvious.
#     """
#     if the_type in (str, int, list, dict, bool, float, date, datetime, timedelta):
#         return the_type.__name__
    
#     return "{} id".format(the_type.__name__)

def _disp(the_value):
    if isinstance(the_value, date):
        return the_value.strftime("%Y-%m-%d")
    
    if isinstance(the_value, datetime):
        return the_value.strftime("%Y-%m-%d %H:%M:%S")
    
    return the_value

def build_value_tree(the_trigger_script, the_owner=None):
    if the_owner is None:
        the_owner = user_f.get_user(the_trigger_script.owner)
        
        # We use this so we don't edit the actual date and thus
        # override it, if we leave it we can get an error
        # as join_date is nullable and we call .strftime on it
        owner_join_date = the_owner.join_date
        if owner_join_date is None:
            owner_join_date = date.today()
    
    data = []
    d = lambda name, line_type, example, description: {"key":name, "type":line_type.__name__, "example": example, "description":description}
    
    the_trigger = get_trigger(the_trigger_script.trigger)
    data.append({
        "key": "trigger",
        "type": " ",
        "example": " ",
        "description": " ",
        "values": [{"key":name, "type":ty.__name__, "example": _disp(the_trigger.example_inputs[0][name]), "description":desc} for (name, ty, desc) in the_trigger.outputs],
    })
    
    data.append({
        "key": "owner",
        "type": " ",
        "example": " ",
        "description": " ",
        "_values": [
            d("id", int, the_owner.id, "ID of script owner"),
            d("username", str, the_owner.username, "Username of the script owner"),
            d("display_name", str, the_owner.display_name, "Username of the script owner"),
            d("email", str, the_owner.email, "Username of the script owner"),
            d("join_date", date, owner_join_date.strftime("%Y-%m-%d"), "Username of the script owner"),
        ],
    })
    
    script_data = json.loads(the_trigger_script.actions)
    for a in script_data['actions']:
        action_data = []
        the_action = get_action(a['action'])
        for oname, otype, olabel in the_action.outputs:
            action_data.append(d(oname, otype, _disp(the_action.example_inputs[0][1][oname]), olabel))
        
        data.append({
            "key": "{} ({})".format(a['name'], a['label']),
            "type": " ",
            "example": " ",
            "description": " ",
            "_values": action_data,
        })
    
    return json.dumps([{"key":"Values", "values":data}])

def convert(raw_data, data_type):
    """Takes a raw string of data and converts it into the correct data type"""
    
    if data_type == str:
        return raw_data
    
    elif data_type == int:
        return str(int(raw_data))
    
    elif data_type == float:
        return str(float(raw_data))
    
    elif data_type == list:
        return list(raw_data.split(","))
        
    # elif data_type == dict:
    #     formatted_data = dict()
    
    else:
        raise KeyError("No handler for data type of {} for {}".format(data_type, data_name))
    
    return formatted_data