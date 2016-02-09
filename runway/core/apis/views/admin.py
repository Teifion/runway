from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ..lib import api_f
from ...system.lib import user_f
from ...lib import common

def home(request):
    layout      = common.render("viewer")
    
    keys = list(api_f.get_key_list())
    user_key = None
    
    for u, k in keys:
        if k.user == request.user.id:
            user_key = k.key
    
    if user_key is None:
        user_key = api_f.grant(request.user.id)
        keys = list(api_f.get_key_list())
    
    return dict(
        title       = "APIs: Home",
        layout      = layout,
        keys        = keys,
        handlers    = api_f._handlers,
        user_key    = user_key,
    )

def grant(request):
    username = request.params['username']
    
    user_id = user_f.get_userid(username)
    
    if user_id is None:
        raise common.GracefulException("Username not found", """I'm very sorry. We were unable to find a user with the name '{}'""".format(username), category="Not found")
    
    api_f.grant(user_id)
    return HTTPFound(request.route_url('api.admin.home'))
    
def revoke(request):
    key_id = int(request.matchdict['key_id'])
    api_f.revoke(key_id)
    
    return HTTPFound(request.route_url('api.admin.home'))
