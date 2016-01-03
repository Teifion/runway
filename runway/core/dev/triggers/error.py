from datetime import datetime
from ....core.triggers import Trigger
from ....core.system.models.user import User

class ErrorTrigger(Trigger):
    """
    This fires when an error is logged.
    """
    
    name = "dev_error_trigger"
    group = "Dev"
    label = "Runway error"
    description = "This fires when an error is logged."
    documentation = ""
    location = __file__
    
    # The data the trigger is expected to produce
    outputs = (
        ("log_id", int, "The ID of the log which was just added to the database"),
        ("timestamp", datetime, "The datetime of the error"),
        ("path", str, "The path being accessed"),
        ("user", User, "The ID of the user in question"),
        ("description", float, "The message that the exception genreated"),
        ("traceback", str, "The traceback of the page"),
        ("data", str, "The data submitted by the user"),
    )
    
    permissions = ["developer"]
    
    example_inputs = [{
        "log_id":      1,
        "timestamp":   datetime(2016, 1, 4, 12, 33, 14),
        "path":        "admin/home",
        "user":        1,
        "description": "Error msg description",
        "traceback":   "<<traceback>>",
        "data":        '{"arg1":1,"arg2":"2"}'
    }]
    
    example_outputs = [{
        "log_id":      1,
        "timestamp":   datetime(2016, 1, 4, 12, 33, 14),
        "path":        "admin/home",
        "user":        1,
        "description": "Error msg description",
        "traceback":   "<<traceback>>",
        "data":        '{"arg1":1,"arg2":"2"}',
    }]
    
    def __call__(self, log_id, timestamp, path, user, description, traceback, data):
        """
        The input data is essentially an error log constructor
        """
        
        return {
            "log_id": log_id,
            "timestamp": timestamp,
            "path": path,
            "user": user,
            "description": description,
            "traceback": traceback,
            "data": data
        }
