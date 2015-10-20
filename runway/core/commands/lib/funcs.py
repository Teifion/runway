from collections import defaultdict
import types

commands = defaultdict(list)

_command_dict = {}

# import logging
# log = logging.getLogger(__name__)

is_func = lambda c: isinstance(c, types.FunctionType) or isinstance(c, types.LambdaType)

def register_commands(*commands):
    for c in commands:
        if isinstance(c, types.ModuleType):
            items = map(lambda v: getattr(c, v), dir(c))
            register_commands(*filter(is_func, items))
        
        elif is_func(c):
            if c.__name__[0] != "_":
                _command_dict[c.__name__] = c
            
        else:
            pass


def execute_command(command_name, *args, **kwargs):
    if command_name in _command_dict:
        return _command_dict[command_name](*args, **kwargs)
    
    else:
       raise KeyError("Command by the name of '{}' could not be found".format(command_name)) 
    
    # for handler in hooks[hook_name]:
    #     try:
    #         handler(**kwargs)
    #     except Exception:
    #         log.debug("Tried to run handler of {}".format(str(handler)))
    #         raise

def is_int(value):
    """
    Returns true if the value is an int as a string
    """
    if isinstance(value, int):
        return True
    
    try:
        vint = int(value)
        return str(vint) == value
    except Exception:
        return False

def int_if_int(value):
    """
    Returns as int if it's an int as a string, else it returns the input value
    """
    
    return int(value) if is_int(value) else value
