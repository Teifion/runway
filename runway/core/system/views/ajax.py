from pyramid.httpexceptions import HTTPFound
from ...lib import common
from ..lib import user_f
from ...admin.lib import searches
from ...system.models.user import group_types

def user_search(request):
    username = request.params['username'].strip()
    
    if len(username) < 3:
        return ""
    
    users = searches.by_either_name(username)
    return "\n".join(["{}|{}".format(u.username, u.display_name) for u in users])

def group_search(request):
    username = request.params['username'].strip()
    
    if len(username) < 3:
        return ""
    
    users = searches.by_either_name(username, groups_only=True)
    return "\n".join(["{}|{}".format(u.username, u.display_name) for u in users])

def combo_search(request):
    username = request.params['username'].strip()
    
    if len(username) < 3:
        return ""
    
    users = searches.by_either_name(username, allow_groups=True)
    return "\n".join(["{}|{}".format(u.username, u.display_name) for u in users])
