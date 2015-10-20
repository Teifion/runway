from ..lib import api_f

from ...base import DBSession
from ...system.models.user import User
from ...system.lib import user_f
import json

def api_request(request):
    the_key = api_f.auth(request.params.get('key', ''))
    
    if the_key is None:
        return "Key not found"
    
    request_mode = request.params.get('request', '')
    
    if request_mode in api_f.handlers:
        request.user = user_f.get_user(the_key.user)
        
        func, permission = api_f.handlers[request_mode]
        
        if permission in request.user.permissions():
            return func(request)
        else:
            return "You do not have permission to access the API function of '{}'".format(request_mode)
    
    else:
        return "Request mode of '{}' is not valid".format(request_mode)
