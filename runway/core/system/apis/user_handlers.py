from ...base import DBSession
from ..lib import auth
from ..models.user import User
import json
from ....core.apis import APIHandler

class UserList(APIHandler):
    name = "system.users"
    group = "System"
    label = "Users"
    description = """Returns a list of all the users in the system."""
    documentation = """HTML DOC"""
    location = __file__
    
    permissions = ["developer"]
    
    def __call__(self, request, test_mode=False):
        map_func = lambda u: {'id':u.id, 'username':u.username, 'display_name':u.display_name, 'email':u.email}
        user_data = map(map_func, DBSession.query(User))
        
        return json.dumps(list(user_data))

class PermissionGroups(APIHandler):
    name = "system.user_permission_groups"
    group = "System"
    label = "User permission groups"
    description = """Returns a list of all the permission groups in the system."""
    documentation = """HTML DOC"""
    location = __file__
    
    permissions = ["developer"]
    
    def __call__(self, request, test_mode=False):
        map_func = lambda ag: {'name':ag.name, 'permissions':list(ag.permissions)}
        
        # While it's in dev I don't need anybody knowing about this
        group_data = filter(
            lambda v: 'guardian' not in v['name'] and 'guardian' not in v['permissions'],
            map(map_func, auth.RootFactory.__acl__)
        )
        
        return json.dumps(list(group_data))
