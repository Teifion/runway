from ...apis.lib import api_f

from ...base import DBSession
from ..lib import auth
from ..models.user import User
import json

def users(request):
    map_func = lambda u: {'id':u.id, 'username':u.username, 'display_name':u.display_name, 'email':u.email}
    user_data = map(map_func, DBSession.query(User))
    
    return json.dumps(list(user_data))

def groups(request):
    map_func = lambda ag: {'name':ag.name, 'permissions':list(ag.permissions)}
    
    # While it's in dev I don't need anybody knowing about this
    group_data = filter(
        lambda v: 'guardian' not in v['name'] and 'guardian' not in v['permissions'],
        map(map_func, auth.RootFactory.__acl__)
    )
    
    return json.dumps(list(group_data))
