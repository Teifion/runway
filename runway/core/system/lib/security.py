from . import user_f
from ..models.user import PartialLogin
from ...base import DBSession
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember

import re
import string
import random
import json
from collections import namedtuple

SecurityCheck = namedtuple('SecurityCheck', ['label', 'show_data', 'login_function', 'partial_function'])

# def _disabled_account_login(request, the_check):
#     return "This account is disabled"

def _ip_whitelist(request, the_check):
    # We need to do this for the testing, it doesn't provide a remote_addr
    if request.remote_addr is None:
        request.remote_addr = "127.0.0.1"
    
    regex = re.compile(the_check.data.replace(".", "\\.").replace("*", "[0-9]*"))
    
    if regex.search(request.remote_addr) is None:
        return "You are not authorised to login from {}".format(request.remote_addr)

def _ip_blacklist(request, the_check):
    # We need to do this for the testing, it doesn't provide a remote_addr
    if request.remote_addr is None:
        request.remote_addr = "127.0.0.1"
    
    regex = re.compile(the_check.data.replace(".", "\\.").replace("*", "[0-9]*"))
    
    if regex.search(request.remote_addr) != None:
        return "You are not authorised to login from {}".format(request.remote_addr)

def _challenge_response(request, the_partial):
    if "challenge_response" in request.params:
        predicate = lambda c: c.check == 'challenge_response' and c.data == the_partial.data['challenge']
        selected_challenge = tuple(filter(predicate, user_f.get_user_security_checks(the_partial.user)))[0]
        
        correct_answer = selected_challenge.data.split(',')[1]
        
        if correct_answer == request.params['challenge_response']:
            remaining_parts = the_partial.remaining.split(",")
            the_partial.remaining = ",".join(remaining_parts[1:])
            
            if remaining_parts[1:] == []:
                result = successful_login(request, the_partial.user)
                remove_partial(the_partial.hash)
                return result
        
        else:
            return {
                'mode':'challenge_response',
                'challenge':selected_challenge,
                'message': ("danger", "Invalid response"),
            }
    
    # Select a challenge for them
    else:
        if 'challenge' not in the_partial.data:
            predicate = lambda c: c.check == 'challenge_response'
            checks = tuple(filter(predicate, user_f.get_user_security_checks(the_partial.user)))
            selected_challenge = random.choice(checks)
            
            the_partial.data['challenge'] = selected_challenge.data
            update_partial(the_partial)
        
        else:
            predicate = lambda c: c.check == 'challenge_response' and c.data == the_partial.data['challenge']
            selected_challenge = tuple(filter(predicate, user_f.get_user_security_checks(the_partial.user)))[0]
        
        return {
            'mode':'challenge_response',
            'challenge':selected_challenge,
        }

_pass = lambda a,b: None
checks = {
    # 'disabled_account': SecurityCheck('Disabled account', False, _disabled_account_login, None),
    'ip_whitelist': SecurityCheck('IP Whitelist', True, _ip_whitelist, None),
    'ip_blacklist': SecurityCheck('IP Blacklist', True, _ip_blacklist, None),
    'challenge_response': SecurityCheck('Challenge - Response', True, _pass, _challenge_response),
}

def get_check_by_label(label):
    for c in checks.values():
        if c.label == label:
            return c

_check_order = (
    'Challenge - Response',
)

def login(request):
    username = request.params['username'].strip()
    password = request.params['password']
    result = "complete"
    partials = set()
    
    try:
        user_id = user_f.attempt_login(username, password)
        
        # Grab the security checks
        # check check check check check check
        user_checks_list = tuple(user_f.get_user_security_checks(user_id))
        
        for user_check in user_checks_list:
            check_object = checks[user_check.check]
            result = check_object.login_function(request, user_check)
            
            # If they have partial requirements then lets do those
            if check_object.partial_function != None:
                partials.add(check_object.label)
            
            if result != None:
                raise Exception(result)
        
    except Exception as e:
        return "failure", e.args[0]
    
    if len(partials) > 0:
        return user_id, new_partial(user_id, request.remote_addr, partials)
    
    return user_id, result

def new_partial(user_id, ip, items):
    DBSession.query(PartialLogin).filter(PartialLogin.user == user_id).delete()
    
    saltable = string.ascii_letters + string.digits
    hash_str = "".join([random.choice(saltable) for x in range(32)])
    
    DBSession.add(PartialLogin(
        user      = user_id,
        ip        = ip,
        remaining = ",".join(items),
        hash      = hash_str,
    ))
    
    return hash_str

def get_partial(hash_str):
    the_partial = DBSession.query(PartialLogin).filter(PartialLogin.hash == hash_str).first()
    the_partial.data = json.loads(the_partial.data_str)
    return the_partial

def remove_partial(hash_str):
    return DBSession.query(PartialLogin).filter(PartialLogin.hash == hash_str).delete()

def update_partial(the_partial):
    the_partial.data_str = json.dumps(the_partial.data)
    return DBSession.add(the_partial)

def perform_partial(request):
    hash_str = request.params['h']
    
    the_partial = get_partial(hash_str)
    remaining_parts = the_partial.remaining.split(",")
    
    # Find out what the currently expected check is
    for c in _check_order:
        if c in remaining_parts:
            current_check = get_check_by_label(c)
            return current_check.partial_function(request, the_partial)
    
    # What if we don't find one?
    raise Exception("Could not find a current check.\nStr: {}\nSplit: {}".format(
        the_partial.remaining,
        str(remaining_parts),
    ))

def successful_login(request, user_id, came_from=None):
    if came_from == None:
        came_from = request.route_url('/')
    user_f.update_session_ip(user_id, session_ip=request.remote_addr)
    headers = remember(request, user_id, max_age = 60*60*24*7*9999)
    return HTTPFound(location = came_from, headers = headers)
