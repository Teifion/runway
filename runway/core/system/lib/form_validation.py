from ...lib.common import GracefulException
from datetime import datetime, date

type_type = type(str)

# AttributeError
def convert_to_stripstr(v):
    return v.strip()

def convert_to_int(v):
    return int(v)

def convert_to_float(v):
    return float(v)

def convert_to_date(v):
    return date(v)

def convert_to_datetime(v):
    return datetime(v)

type_conversion = {
    str: str,
    "stripstr": convert_to_stripstr,
    int: convert_to_int,
    float: convert_to_float,
    date: convert_to_date,
    datetime: convert_to_datetime,
}

def validate_form(request, *fields):
    """
    Given a request object and a definition for that form it will validate all
    elements and pass back either a dictionary of the validated values
    or will raise a list of the errors.
    
    *fields is a tuple/list of fields expected, each field will have a name,
    a conversion and a list of validation rules such as below:
    
    validate_form(request,
        ("name", str, non_empty, min_length(3)),
        ("age", int, non_zero),
        ("role", str, allowed_values("user", "moderator", "admin")),
    )
    """
    errors = {}
    results = {}
    
    for pf in fields:
        name = pf[0]
        conversion = pf[1]
        funcs = pf[2:]
        
        name_errors = []
        
        try:
            value = type_conversion[conversion](request.params[name])
        except Exception:
            errors[name] = ["Unable to convert the value '{}' into correct format".format(request.params[name].strip())]
            continue
        
        # Now validate against each of the functions
        for f in funcs:
            fresult = f(value)
            
            if fresult != True:
                name_errors.append(f.__doc__)
        
        if name_errors != []:
            errors[name] = name_errors
        
        results[name] = value
    
    return results, errors


def raise_graceful(results, errors, msg=""):
    """
    Takes the results and errors from a form validation and prints them in a nice
    graceful exception.
    
    Optionally a message can be included which will be prefixed to the start of the output.
    """
    error_list = []
    error_count = 0
    
    for k, v in errors.items():
        error_list.append("<br /><strong>{}</strong> ({})".format(k, results[k]))
        
        for e in v:
            error_list.append("&nbsp;&nbsp;&nbsp;{}".format(e))
            error_count += 1
    
    # If the message is non-empty then extend it with a pair of line breaks
    if msg != "":
        msg = msg + "<br /><br />"
    
    raise GracefulException("Form validation errors",
        """{}There {}:
        <br />
        {}
        """.format(
            msg,
            ("were {} errors".format(error_count) if error_count != 1 else "was a single error"),
            "<br />".join(error_list)
        ),
        category="input"
    )





"""
Validation functions:
These are a set of functions which can be used to validate input

"""

def non_empty(value):
    "Expected a non-empty value, make sure you've not left this field accidentally blank"
    return value != ""

def minlength(l):
    def f(value):
        "Expected a value with a length of at least {}".format(l)
        return len(value) >= l

def maxlength(l):
    def f(value):
        "Expected a value with a length of at most {}".format(l)
        return len(value) <= l

