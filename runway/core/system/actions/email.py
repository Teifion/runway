from ....core.triggers import Action

class Email(Action):
    name = "system_email"
    group = "System"
    label = "Email"
    description = """Takes multiple inputs and formats them according to a scheme. Ultimately just a wrapper for the string.format function in Python."""
    documentation = """HTML DOC"""
    
    # The data the trigger is expected to produce
    inputs = (
        ("recipient1", str, ""),
        ("recipient2", str, ""),
        ("recipient3", str, ""),
        ("subject", str, ""),
        ("content", str, ""),
    )
    
    outputs = (
        # ("formatted_string", str, "The result of applying format to the unformatted string."),
    )
    
    permissions = ["developer"]
    
    examples = [
        (
            {"recipient1":"user@email.com", "recipient2":"user@email.com", "recipient3":"user@email.com", "subject":"Subject", "content":"Email content", "args":["1", "2", "3"]},
            {}
        ),
    ]
    
    def __call__(self, recipient1, recipient2, recipient3, subject, content, test_mode=False):
        recipients = recipient1.split(";") + recipient2.split(";") + recipient3.split(";")
        
        print("\n\n")
        print(str(recipients))
        print(str(subject))
        print(str(content))
        print("\n\n")
        
        return {}
        raise Exception("Not implemented")
