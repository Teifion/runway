from ..lib import api_f

from ...base import DBSession
from ...system.models.user import User
from ...system.lib import user_f
import json

def api_request(request):
    request.api_bypass_tweens = True
    
    the_key = api_f.auth(request.params.get('key', ''))
    
    if the_key is None:
        return "Key not found"
    
    request_mode = request.params.get('request', '')
    
    if request_mode in api_f._handlers:
        request.user = user_f.get_user(the_key.user)
        
        the_handler = api_f._handlers[request_mode]
        
        for p in the_handler.permissions:
            if p not in request.user.permissions():
                return "You do not have permission to access the API function of '{}'".format(request_mode)
        
        return the_handler()(the_handler, request)
        
    
    else:
        return "Request mode of '{}' is not valid".format(request_mode)
