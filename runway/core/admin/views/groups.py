from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from ....core.system.js_widgets import UserPicker
# import io
# import csv

from ..lib import searches, admin_f
from ...system.lib import user_f
from ...lib import common
from ...system.models.user import group_types

# from datetime import date

def list_groups(request):
    layout      = common.render("viewer")
    
    results = user_f.get_groups()
    
    return dict(
        title       = "Admin: Groups",
        layout      = layout,
        results     = results,
    )

def create(request):
    layout      = common.render("viewer")
    
    response = dict(
        title       = "Admin: Quick add group",
        layout      = layout,
    )
    
    if "groupname" in request.params:
        the_group = admin_f.blank_group()
        the_group.display_name = request.params["groupname"].strip()
        the_group.username = admin_f.new_groupname(the_group.display_name)
        the_group.group_owner = request.user.id
        
        if the_group.username == "":
            response['message'] = "danger", "No group name was provided"
            return response
        
        try:
            user_f.save(the_group, flush=True)
        except Exception as e:
            if e.args[0][:33] == "(UniqueError) duplicate key value":
                response['message'] = "danger", "That group name already exists"
                return response
            
            raise
        
        # Now get the latest user
        new_user = user_f.get_user(the_group.username, allow_groups=True)
        return HTTPFound(location=request.route_url('admin.groups.edit', group_id=new_user.id))
    
    response['message'] = "danger", "No username was provided"
    return response

def view(request):
    layout      = common.render("viewer")
    
    page = int(request.params.get('page', 1))
    
    results = []
    if "username" in request.params:
        results = tuple(searches.by_username(request.params['username'], page=page))
    
    if len(results) == 1 and 'page' not in request.params:
        return HTTPFound(location=request.route_url('admin.user.edit', user_id=results[0].id))
    
    return dict(
        title       = "Admin: View group",
        layout      = layout,
        results     = results,
        page        = page,
    )

def edit(request):
    layout      = common.render("viewer")
    
    group_id = int(request.matchdict['group_id'])
    the_group, the_owner = user_f.get_group_and_owner(group_id)
    message = None
    
    UserPicker(request)
    members = tuple(user_f.get_users(the_group.id))
    
    # admin_f.check_group_edit_permissions(request, the_group, members)
    if the_group.group_owner != request.user.id and "admin.su" not in request.user.permissions():
        return HTTPFound(location=request.route_url('admin.groups.view', group_id=the_group.id))
    
    if 'group_name' in request.params:
        # New username? Better check it's not taken
        new_username = request.params['group_name'].strip()
        
        # New owner? Lets check on that too
        owner_name = request.params['owner']
        owner_id = user_f.get_userid(owner_name, allow_groups=False)
        
        if new_username != the_group.username and user_f.get_userid(new_username, allow_groups=True) != None:
            message = "danger", "There is already a group with that username, no changes have been saved"
            
        elif owner_id == None:
            message = "danger", "There is no user by the name of '{}', no changes have been saved".format(owner_name)
            
        else:
            the_group.username = new_username.lower()
            the_group.display_name = new_username
            
            # We need to get this so the form renders correctly
            the_owner = user_f.get_user(owner_id)
            the_group.group_owner = owner_id
            
            the_group.group_edit = int(request.params['group_edit'])
            the_group.group_view = int(request.params['group_view'])
        
        if message == None:
            message = "success", "Changes saved"
            user_f.save(the_group)
    
    return dict(
        title       = "Admin: Edit group",
        layout      = layout,
        the_group   = the_group,
        the_owner   = the_owner,
        message     = message,
        common      = common,
        
        members     = members,
        group_types = {k:v for k,v in enumerate(group_types)},
    )

def remove(request):
    pass

def add_member(request):
    group_id = int(request.matchdict['group_id'])
    the_group = user_f.get_user(group_id, allow_groups=True)
    members = tuple(user_f.get_users(the_group.id))
    
    admin_f.check_group_edit_permissions(request, the_group, members)
    
    usernames = (u.strip() for u in request.params['usernames'].replace(",", "\n").split("\n"))
    user_ids = user_f.get_user_ids_by_name(*usernames)
    
    member_ids = [u.id for u in members]
    ids_to_add = filter(lambda u: u not in member_ids, user_ids)
    
    user_f.add_users_to_group(group_id, *ids_to_add)
    return HTTPFound(location=request.route_url('admin.groups.edit', group_id=group_id))
    
def remove_member(request):
    group_id = int(request.matchdict['group_id'])
    the_group = user_f.get_user(group_id, allow_groups=True)
    members = tuple(user_f.get_users(the_group.id))
    
    admin_f.check_group_edit_permissions(request, the_group, members)
    
    userids = [int(u) for u in request.params['userids'].split(",")]
    user_f.remove_users_from_group(group_id, *userids)
    
    return HTTPFound(location=request.route_url('admin.groups.edit', group_id=group_id))

def search(request):
    layout      = common.render("viewer")
    
    results = []
    if "group_name" in request.params:
        search_name = request.params['group_name'].strip().lower()
        
        results = tuple(searches.find_groups(request.params['group_name']))
        
        print("\n\n")
        print(results)
        print("\n\n")
    
    if len(results) == 1:
        return HTTPFound(location=request.route_url('admin.groups.edit', group_id=results[0].id))
    
    return dict(
        title       = "Admin: Search groups",
        layout      = layout,
        results     = results,
    )