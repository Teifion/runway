from ....core.triggers import Action
from ....core.system.lib import email_f

class Email(Action):
    name = "system_email"
    group = "System"
    label = "Email"
    description = """Takes multiple inputs and formats them according to a scheme. Ultimately just a wrapper for the string.format function in Python."""
    documentation = """HTML DOC"""
    location = __file__
    
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
        email_f.send_email(recipients, subject, text_message=content, test_mode=test_mode)


# {"actions": [{"input_map": {"user": "trigger.user"}, "name": "system_get_user_1", "action": "system_get_user", "label": "The user involved"}, {"input_map": {"kwargs": {"": "\"\"", "description": "trigger.description", "data": "trigger.data", "timestamp": "trigger.timestamp", "log_id": "trigger.log_id", "traceback": "trigger.traceback", "user": "system_get_user_1.username", "path": "trigger.path"}, "unformatted_string": "\"<strong>{user}</strong>: {path}\r\n{timestamp}\r\n{data}\r\n\r\n{description}\r\n\r\n{traceback}\r\n\""}, "name": "system_formatter_1", "action": "system_formatter", "label": "Formatter for email"}, {"input_map": {"recipient2": "\"\"", "content": "system_formatter_1.formatted_string", "subject": "\"Runway error: EUI\"", "recipient1": "\"sarkalian@gmail.com\"", "recipient3": "\"\""}, "name": "system_email_1", "action": "system_email", "label": "Emailer"}], "conditions": []}