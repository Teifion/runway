import re
from collections import namedtuple

from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
)


from zope.interface import implementer
from pyramid.interfaces import IAuthorizationPolicy
from pyramid.location import lineage
from pyramid.compat import is_nonstr_iter

from pyramid.security import (
    ACLAllowed,
    ACLDenied,
    Allow,
    Deny,
    Everyone,
)

find_special = re.compile(r"[|&\^]")

class PermissionSet(object):
    """A set of permissions held by a user. You can then use 'in' to
    determine if a set of permission requirements match"""
    def __init__(self, permissions):
        super(PermissionSet, self).__init__()
        self.permissions = set(permissions)
    
    def check(self, required):
        if required is None:
            return True
        
        if required in ("dev", "devel"):
            raise Exception("No permission set of '{}', did you mean 'developer'?".format(required))
        
        return required in self.permissions
    
    def __str__(self):
        return str(self.permissions)
    
    def __eq__(self, other):
        return self.check(other)
    
    def __contains__(self, key):
        return self.check(key)
    
    def __iter__(self):
        return (p for p in self.permissions)
    
    def __or__(self, other):
        if isinstance(other, set):
            self.permissions.update(other)
            return self
        raise Exception("No handler for other type of %s" % type(other))

class AuthGroup(object):
    def __init__(self, allowance, name, permissions, namespace="", rank=1, label=None, **kwargs):
        super(AuthGroup, self).__init__()
        
        if label == None:
            self.label = name
        
        self.namespace = namespace
        if self.namespace != "":
            permissions = set(["{}.{}".format(namespace, p) for p in permissions])
            permissions.add(namespace)
            
            self.label = "({}) {}".format(self.namespace, self.label)
            
            name = "{}.{}".format(namespace, name)
        
        self.allowance = allowance
        self.name = name
        self.permissions = set(permissions)
        self.rank = rank
        
        # Allows for custom behaviour
        self.kwargs = kwargs
            
    def __iter__(self):
        return (x for x in (self.allowance, self.name, self.permissions))

user_groups = []
permissions = []
global_permissions = ["view", "loggedin"]
class RootFactory(object):
    __acl__ = [
        AuthGroup(Allow, 'developer',   {'developer', 'errors', 'su', 'backup'}, rank=5, system_only=True),
        AuthGroup(Allow, 'su',          {'su'}, rank=4),
        
        AuthGroup(Allow, Everyone,      {'view'}, rank=0, system_only=True),
        AuthGroup(Allow, Authenticated, {'loggedin'}, rank=0, system_only=True),
        
        # Dev related view used to test error display and perform backups
        AuthGroup(Allow, 'errors',      {'errors'}, rank=5),
        AuthGroup(Allow, 'backup',      {'backup'}, rank=5),
    ]
    
    # Create a developers group which has all the permissions
    # also add most of those permissions to the su
    # finally, also build up some lists for lookup purposes
    for p, name, perms in __acl__:
        permissions.extend(perms)
        user_groups.append(name)
    
    def __init__(self, request):
        pass

def add(namespace, group, ag_permissions, rank=1, label=None, action=Allow, **kwargs):
    if action == "Allow": action = Allow
    
    ag = AuthGroup(action, group, ag_permissions, namespace, rank, label, **kwargs)
    RootFactory.__acl__.append(ag)
    
    RootFactory.__acl__[0].permissions.update(ag.permissions)
    RootFactory.__acl__[1].permissions.update(ag.permissions)
    
    permissions.extend(ag_permissions)
    user_groups.append(group)
    
    return ag_permissions

group_lookup = {}
ag_lookup = {}
def init():
    RootFactory.__acl__[3].permissions.update(set(global_permissions))
    
    for auth_group in RootFactory.__acl__:
        group_lookup[auth_group.name] = tuple(auth_group.permissions)
        ag_lookup[auth_group.name] = auth_group
