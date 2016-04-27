from datetime import datetime, date
import re
from collections import OrderedDict, defaultdict
import math
import base64
import html
import json
import calendar
from ..themes.lib.themes_f import render

class GracefulException(Exception):
    """The idea of this exception is it's an unrecoverable failure from within
    the program but we know enough about the cause to provide a useful
    error message to the user rather than simply running around
    like a headless chicken.
    """
    def __init__(self, title, message, log_anyway=False, echo_input=False, category=""):
        super(GracefulException, self).__init__()
        self.title = title
        self.message = message
        self.echo_input = echo_input
        
        self.log_anyway = log_anyway
        
        self.category = category
        
        # For when we're using the CLI
        self.args = ["\n\n" + message]

def as_graceful(e, title="There was an error", category="default", log_anyway=False, echo_input=False):
    """Takes an exception e and returns it as a Graceful error"""
    return GracefulException(title=title, message=e.args[0], category=category, log_anyway=log_anyway, echo_input=echo_input)

# # Appends "st, nd, rd, th" to the relevant days of the month
# def display_date(format_string="%d of %B", the_date=None):
#     if the_date == None:
#         the_date = datetime.datetime.today()
    
#     day = the_date.day
#     format_string = format_string.replace("%d", "%d{}".format(th_of_month(day)))
#     return the_date.strftime(format_string)

# # A shorthand to display_date but designed for timestamps
# def display_datetime(format_string="%d of %B at %H:%M", the_date=None):
#     return display_date(format_string, the_date)

# def th_of_month(day):
#     if int(day) in (1, 21, 31): return "st"
#     elif int(day) in (2, 22, 32): return "nd"
#     elif int(day) in (3, 23, 33): return "rd"
#     else: return "th"

# # Output a HTML checkbox
# def check_box(name, checked=False, custom_id=None, value="True"):
#     output = ['<input type="checkbox" name="{}" value="{}"'.format(name, value)]
    
#     if checked:
#         output.append('checked="checked"')
    
#     if custom_id != None:   output.append('id="{}"'.format(custom_id))
#     else:                   output.append('id="{}"'.format(name))
    
#     output.append('/>')
#     return " ".join(output)

# def radio_button(name, custom_id, checked=False, value="True"):
#     output = ['<input type="radio" name="{}" value="{}" id="{}"'.format(name, value, custom_id)]
    
#     if checked:
#         output.append('checked="checked"')
    
#     output.append('/>')
#     return " ".join(output)

_filter_type = filter(lambda v: v, [])
def _sort_elements(sequence, element_property="name", reverse=False, as_list=False):
    """Sorts the elements of a dictionary or list while preserving their numerical order"""
    new_sequence = OrderedDict()
    
    if type(sequence) == type(_filter_type):
        sequence = tuple(sequence)
    
    if type(sequence) == set:
        sequence = list(sequence)
    
    if type(sequence) in (list, tuple):
        true_sequence = list(sequence)
        ordered_sequence = list(sequence)
        ordered_sequence.sort()
        return ordered_sequence
        
        # for i in ordered_sequence:
        #     new_sequence[true_sequence.index(i)] = i
    
    elif type(sequence) in (dict, OrderedDict, defaultdict):
        try:
            reverse_dict = {v:k for k, v in sequence.items()}
            ordered_sequence = [v for k, v in sequence.items()]
            ordered_sequence.sort()

            for i in ordered_sequence:
                new_sequence[reverse_dict[i]] = i
        
        except TypeError as e:
            # We need to use the element_property
            reverse_dict = {v.__dict__[element_property]:k for k, v in sequence.items()}
            ordered_sequence = [v.__dict__[element_property] for k, v in sequence.items()]
            ordered_sequence.sort()
        
            for i in ordered_sequence:
                new_sequence[reverse_dict[i]] = i
        
        except Exception as e:
            raise
    
    else:
        raise Exception("Cannot sort type: %s" % type(sequence))
    
    # Flip it about!
    if reverse:
        r = OrderedDict()
        keys = list(new_sequence.keys())
        keys.reverse()
        for k in keys:
            r[k] = new_sequence[k]
        
        new_sequence = r
    
    # As a list?
    if as_list:
        new_sequence = [v for k,v in new_sequence.items()]
    
    return new_sequence

# def select_box(name, iterator, selected="", sort=True, css_class="form-control", custom_id="!", onchange="", style="", tab_index=None):
#     output = ['<select name="{name}" style="{style}" {custom_id}onchange="{onchange}" class="{css_class}"'.format(
#         name = name,
#         custom_id = 'id="%s" ' % (custom_id if custom_id != "!" else name),
#         onchange  = onchange,
#         style     = style,
#         css_class = css_class,
#     )]
    
#     if tab_index != None:
#         output.append('tabIndex="{}"'.format(tab_index))
    
#     output.append('>')
    
#     if sort:
#         elements = _sort_elements(elements, element_property)
    
#     for k, v in iterator:
        
    
#     output.append('</select>')
#     return "".join(output)

_default_filter = lambda kv: True
def select_box(name, elements, selected="", disabled_items=[], sort=True, filterf=_default_filter, **attributes):
    attributes['class'] = attributes.get('css_class', "form-control")
    if 'id' not in attributes: attributes['id'] = name
    
    # It may be we don't want an ID on this entity
    if attributes['id'] is None:
        del(attributes['id'])
    
    disabled_count = 0
    
    output = ['<select name="{}"'.format(name)]
    
    for k, v in attributes.items():
        output.append(' {}="{}"'.format(k, v))
    
    output.append('>')
    
    # Sort?
    if sort:
        elements = _sort_elements(elements)
    
    # Is it a list/tuple or dictionary
    if type(elements) in (list, tuple):
        iterator = ((e,e) for e in elements)
    else:
        iterator = elements.items()
    
    for k, v in filter(filterf, iterator):
        if type(v) not in (str, int):
            v = v.__dict__[element_property]
        
        is_selected = ""
        try:
            if int(selected) == int(k):
                is_selected = 'selected="selected"'
        except Exception:
            if selected == k:
                is_selected = 'selected="selected"'
        
        if k in disabled_items:
            disabled_count += 1
            output.append('<option value="disabled_{}" disabled="disabled">&nbsp;</option>'.format(disabled_count))
            continue
        
        output.append('<option value="{}" {}>{}</option>'.format(k, is_selected, html.escape(v)))
    
    output.append('</select>')
    return "".join(output)

# def string_to_tuple(the_string, to_int=False):
#     """Takes a string and converts it to a list using both commas and spaces as delimiters.
#     It also removes any empty strings"""
#     the_string = the_string.replace(",", "\n").replace(" ", "\n")
    
#     if to_int:
#         return tuple(filter(
#             bool,
#             [int(s.strip()) for s in the_string.split("\n") if s.strip() != ""]
#         ))
#     else:
#         return tuple(filter(
#             bool,
#             [s.strip() for s in the_string.split("\n")]
#         ))

def string_to_datetime(the_string, default=None):
    """Takes a date represented as a string and returns a datetime"""
    attempts = (
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M',
        '%Y-%m-%d',
        
        '%H:%M:%S %d/%m/%Y',
        '%H:%M %d/%m/%Y',
        '%d/%m/%Y',
    )
    
    for attempt_format in attempts:
        try:
            return datetime.strptime(the_string, attempt_format)
        except Exception as e:
            pass
    
    return default
    
    # try:
    #     return datetime.strptime(the_string, '%Y-%m-%dT%H:%M:%S')
    # except:
    #     try:
    #         return datetime.strptime(the_string, '%Y-%m-%d')
    #     except:
    #         return default
        

def string_to_date(the_string, default=None):
    dt = string_to_datetime(the_string)
    try:
        return date(dt.year, dt.month, dt.day)
    except:
        return default

# def string_to_date(the_string, default=None):
#     """Same as above but casts it to a date"""
#     dt = string_to_datetime(the_string, default)
#     if dt == None: return None
#     return datetime.date(year=dt.year, month=dt.month, day=dt.day)

# _timedelta_formatted_hours = re.compile(r"^([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})$")
# _timedelta_formatted_minutes = re.compile(r"^([0-9]{1,2}):([0-9]{1,2})$")
# _timedelta_formatted_seconds = re.compile(r"^([0-9]{1,2})$")
# _timedelta_regexes = (
#     (re.compile(r"(?P<v>[0-9]+) seconds?"), 1),
#     (re.compile(r"(?P<v>[0-9]+) minutes?"), 60),
#     (re.compile(r"(?P<v>[0-9]+) hours?"), 60*60),
#     (re.compile(r"(?P<v>[0-9]+) days?"), 60*60*24),
#     (re.compile(r"(?P<v>[0-9]+) weeks?"), 60*60*24*7),
# )
# def string_to_timedelta(the_string):
#     """Take a string containing time values and return a timedelta"""
    
#     if the_string.strip() == "":
#         return None
    
#     # Numerical formatting
#     num_string = the_string.replace(".", ":").replace(",", ":").strip()
#     r = _timedelta_formatted_hours.match(num_string)
#     if r != None:
#         h, m, s = r.groups()
#         return datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    
#     r = _timedelta_formatted_minutes.match(num_string)
#     if r != None:
#         m, s = r.groups()
#         return datetime.timedelta(minutes=int(m), seconds=int(s))
        
#     r = _timedelta_formatted_seconds.match(num_string)
#     if r != None:
#         s = r.groups()[0]
#         return datetime.timedelta(seconds=int(s))
    
#     # English formatting
#     while "  " in the_string:
#         the_string = the_string.replace("  ", " ")
    
#     seconds = 0
#     for reg, multiplier in _timedelta_regexes:
#         r = reg.search(the_string)
        
#         if r:
#             g = r.groupdict()
#             seconds += int(g['v']) * multiplier
    
#     return datetime.timedelta(seconds=seconds)

# # def timedelta_to_hours(the_delta):
# #     results = 0
# #     t = the_delta.total_seconds()
    
# #     hours = math.floor(t/(60*60))
# #     if hours > 0:
# #         results = hours
# #         t -= (60*60*hours)
    
# #     remainder = t/3600
# #     results += remainder
    
# #     return results

# _roundings = (
#     "years",
#     "months",
#     "days",
#     "hours",
#     "minutes",
#     "seconds",
# )
# def timedelta_to_string(the_delta, round_at="seconds"):
#     rounding = _roundings.index(round_at)
    
#     parts = []
#     t = the_delta.total_seconds()
    
#     years = math.floor(t/(60*60*24*365))
#     if years > 0 and rounding >= _roundings.index("years"):
#         parts.append("%d year%s" % (years, "s" if years != 1 else ""))
#         t -= (60*60*24*365*years)
    
#     months = math.floor(t/(60*60*24*30))
#     if months > 0 and rounding >= _roundings.index("months"):
#         parts.append("%d month%s" % (months, "s" if months != 1 else ""))
#         t -= (60*60*24*30*months)
    
#     days = math.floor(t/(60*60*24))
#     if days > 0 and rounding >= _roundings.index("days"):
#         parts.append("%d day%s" % (days, "s" if days != 1 else ""))
#         t -= (60*60*24*days)
    
#     hours = math.floor(t/(60*60))
#     if hours > 0 and rounding >= _roundings.index("hours"):
#         parts.append("%d hour%s" % (hours, "s" if hours != 1 else ""))
#         t -= (60*60*hours)
    
#     minutes = math.floor(t/(60))
#     if minutes > 0 and rounding >= _roundings.index("minutes"):
#         parts.append("%d minute%s" % (minutes, "s" if minutes != 1 else ""))
#         t -= (60*minutes)
    
#     if t > 0 and rounding >= _roundings.index("seconds"):
#         parts.append("%d seconds" % t)
    
#     return ", ".join(parts)

# def timedelta_shortform(the_delta, use_days=False):
#     if the_delta in ("", None): return "00:00"
    
#     parts = []
#     t = the_delta.total_seconds()
    
#     days = math.floor(t/(60*60*24))
#     if use_days:
#         if days > 0:
#             parts.append(days)
#             t -= (60*60*24*days)
#         else:
#             use_days = False
    
#     hours = math.floor(t/(60*60))
#     if hours > 0:
#         parts.append(hours)
#         t -= (60*60*hours)
#     else:
#         parts.append(0)
    
#     minutes = math.floor(t/(60))
#     if minutes > 0:
#         parts.append(minutes)
#         t -= (60*minutes)
#     else:
#         parts.append(0)
    
#     parts.append(int(t))
    
#     if use_days:
#         if parts[0] == 1:
#             return "{:d} day {:02d}:{:02d}:{:02d}".format(*parts)
#         return "{:d} days {:02d}:{:02d}:{:02d}".format(*parts)
#     if parts[0] > 0:
#         return "{:02d}:{:02d}:{:02d}".format(*parts)
#     if parts[1] > 0:
#         return "00:{:02d}:{:02d}".format(*parts[1:])
#     return "00:00:{:02d}".format(parts[2])

# def floor_time(the_date=None, round_to=60):
#     """
#     http://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object-python
#     Round a datetime object to any time laps in seconds
#     the_date : datetime.datetime object, default now.
#     round_to : Closest number of seconds to round to, default 1 minute."""
    
#     if the_date == None: the_date = datetime.datetime.now()
#     if type(round_to) == datetime.timedelta:
#         round_to = round_to.total_seconds()
    
#     seconds = (the_date - the_date.min).seconds
#     # // is a floor division, not a comment on following line
#     rounding = (seconds + round_to/2) // round_to * round_to
#     return the_date + datetime.timedelta(0, rounding-seconds, -the_date.microsecond)

def encode(*args, **kwargs):
    args = list(args) + ["{}::{}".format(k,v) for k,v in kwargs.items()]
    
    result = base64.b64encode("&&".join(args).encode('utf-8'))
    
    return result.decode('utf-8')

def decode(the_string):
    try:
        real = base64.b64decode(the_string.encode('utf-8')).decode('utf-8')
    except Exception as e:
        try:
            real = base64.b64decode(the_string.encode('utf-8') + "=").decode('utf-8')
        except Exception as e2:
            try:
                real = base64.b64decode(the_string.encode('utf-8') + "==").decode('utf-8')
            except Exception as e3:
                raise e
    
    args = []
    kwargs = {}
    for s in real.split("&&"):
        if "::" in s:
            k,v = s.split("::")
            kwargs[k] = v
        else:
            args.append(s)
    
    return args, kwargs

# def get_total(data_list, key=None, default=None):
#     if len(data_list) == 0:
#         return default
    
#     if key == None: v = data_list[0]
#     else:           v = getattr(data_list[0], key)
    
#     if type(v) == str:
#         return ""
        
#     if type(v) == bool:
#         return False
    
#     tot = None
#     for d in data_list:
#         if key == None: v = d
#         else:           v = getattr(d, key)
            
#         if tot == None:
#             tot = v
#         else:
#             tot += v
    
#     return tot

# def get_average(data_list, key=None, default=None):
#     if len(data_list) == 0:
#         return default
    
#     if key == None: v = data_list[0]
#     else:           v = getattr(data_list[0], key)
    
#     if type(v) == str:
#         return ""
        
#     if type(v) == bool:
#         return False
    
#     tot = get_total(data_list, key, default)
#     return tot/len(data_list)

def dumps(obj, max_prop_len=120, print_string=True):
    result = []
    
    if print_string:
        output_value = print
        output_value("\n\n")
    else:
        output_value = result.append
    
    output_value(str(obj))
    for k in dir(obj):
        v = getattr(obj, k)
        
        try:
            vstr = repr(v)[0:max_prop_len]
        except Exception:
            try:
                vstr = str(v)[0:max_prop_len]
            except Exception:
                vstr = "Type = %s" % str(type(v))[0:max_prop_len]
        
        output_value("{:30}{}".format(k, vstr))
    output_value("\n\n")
    
    if print_string:
        output_value("\n\n")
    else:
        return result

def split_and_clean(the_string, as_ints=False):
    """
    Takes a string of comma and/or newline separated string and
    return a list of non-empty strings
    """
    
    result = filter(
        lambda v: v != "",
        (val.strip() for val in the_string.replace("\n", ",").split(","))
    )
    
    if as_ints:
        return (int(v) for v in result)
    else:
        return result

def json_default(obj):
    """Default JSON serializer."""
    
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    
    if isinstance(obj, set):
        return list(obj)
    
    return None
