from ....core.triggers import Trigger

class ErrorTrigger(Trigger):
    """
    You are required to define the following fields
    
    name -> Machine name of the trigger, I'd suggest the use of a namespace
    label -> Human readable name of the trigger
    description -> Human readable description of the trigger, designed to inform
        end users about what the trigger does and when/where it will fire
    data -> A sequence of 3 length tuples (name, type, description)
    
    Optionally:
    permissions -> A list of permissions required to use this trigger
    examples -> A list of example outputs that could be produced by the trigger
        the first example is used in the dev section to provide blank data
    """
    
    name = "dev_dummy_trigger"
    label = "Error"
    description = "Triggers on the creation of an error log"
    
    # The data the trigger is expected to produce
    outputs = (
        ("field1", int, "Random number between 0 and 1"),
        ("field2", str, "Random string of 5 characters"),
        ("field3", list, "List of 5 random numbers (between 0 and 1)"),
        ("field4", list, "An empty list"),
    )
    
    permissions = ["developer"]
    
    example_inputs = [{}]
    
    examples = [{
        "field1": 0.456,
        "field2": "abcde",
        "field3": [0.11, 0.22, 0.15, 0.98, 0.33],
        "field4": [],
    },
    {
        "field1": 0.999,
        "field2": "zzzzz",
        "field3": [0.99] * 5,
        "field4": [],
    }]
    
    def __call__(self):
        """
        This dummy trigger expects no arguments. However, it's quite possible you'd want
        to add arguments for various things (e.g. ID of user added).
        """
        
        return {
            "field1": random.random(),
            "field2": "".join([random.choice(string.ascii_lowercase) for i in range(5)]),
            "field3": [random.random() for i in range(5)],
        }
