from ....core.triggers import Action

class Formatter(Action):
    name = "system_formatter"
    group = "System"
    label = "Formatter"
    description = """Takes multiple inputs and formats them according to a scheme. Ultimately just a wrapper for the string.format function in Python."""
    documentation = """HTML DOC"""
    location = __file__
    
    # The data the trigger is expected to produce
    inputs = (
        ("unformatted_string", str, "Will be disregarded, exists only for demonstration purposes"),
        ("kwargs", dict, "The strings passed into the format function"),
    )
    
    outputs = (
        ("formatted_string", str, "The result of applying format to the unformatted string."),
    )
    
    permissions = ["developer"]
    
    examples = [
        (
            {"unformatted_string":"{first}, {last}", "kwargs":{"first":"Teifion", "last":"Jordan"}},
            {"formatted_string": "Teifion, Jordan"}
        ),(
            {"unformatted_string":"I want a pony", "kwargs":{}},
            {"formatted_string": "I want a pony"}
        ),
    ]
    
    def __call__(self, unformatted_string, test_mode=False, **kwargs):
        result = unformatted_string.format(**kwargs)
        
        return {
            "formatted_string": result,
        }
