from ....core.triggers import Action

import logging
log = logging.getLogger(__name__)

class DummyAction(Action):
    """
    You are required to define the following fields
    
    name -> Machine name of the trigger, I'd suggest the use of a namespace
    label -> Human readable name of the trigger
    description -> Human readable description of the trigger, designed to inform
        end users about what the trigger does and when/where it will fire
    inputs -> A sequence of 3 length tuples (name, type, description)
        Note: An input named "args" of type list will be treated as a varadic input (*args)
        and the same will apply to "kwargs" of type dict (**kwargs)
    outputs -> A sequence of 3 length tuples (name, type, description), an empty sequence
        indicates no returned values (e.g. an email action)
    examples -> A list of example input to output combinations that could be produced
        by the action, the first example is used in the dev section to provide blank data
    location -> The location of the file itself
    
    Optionally:
    permissions -> A list of permissions required to use this action
    """
    
    name = "triggers_dummy_action"
    group = "Triggers"
    label = "Dummy action"
    description = """A dummy action, it prints a message to the log as DEBUG level.
Additionally it will produce a True boolean and an Integer of value 1."""
    documentation = """A dummy action, it takes stuff and prints it."""
    location = __file__
    
    # The data the trigger is expected to produce
    inputs = (
        ("integer_input", int, "Will be disregarded, exists only for demonstration purposes"),
        ("string_input", str, "Will be disregarded, exists only for demonstration purposes"),
    )
    
    outputs = (
        ("boolean_result", bool, "Will always evaluate to True"),
        ("integer_result", int, "Will always evaluate to 1"),
        ("string_result", int, "Will always evaluate to 1"),
    )
    
    permissions = ["developer"]
    
    examples = [
        (
            dict(integer_input=123, string_input="abc"),
            dict(boolean_result=True, integer_result=1, string_result="DummyAction (TEST MODE) has been called")
        ),(
            dict(integer_input=12*12*12, string_input="zzyyxx"),
            dict(boolean_result=True, integer_result=1, string_result="DummyAction (TEST MODE) has been called")
        ),
    ]
    
    def __call__(self, integer_input, string_input, test_mode=False):
        """
        This dummy action requires an integer and a string input, it will disregarded
        both of them. They exist here only for demonstration purposes.
        
        Normally in an action the results would be dependent on the inputs, in this case
        they are constant purely for demonstration purposes.
        """
        
        if test_mode:
            string_result = "\n\nDummyAction (TEST MODE) has been called successfully with\nint:{}\nstr:{}\n".format(integer_input, string_input)
        else:
            string_result = "\n\nDummyAction has been called successfully with\nint:{}\nstr:{}\n".format(integer_input, string_input)
        
        log.debug(string_result)
        
        return {
            "boolean_result": True,
            "integer_result": 1,
            "string_result": string_result
        }
