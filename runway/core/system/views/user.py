from pyramid.httpexceptions import HTTPFound
from ...lib import common
from ..lib import user_f, user_settings_f
from ...admin.lib import admin_f
from ...system.models.user import group_types
from ....core.system.js_widgets import UserPicker

def control_panel(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    settings_dict = user_settings_f.get_all_settings(request.user.id)
    
    if "change" in request.params:
        for group_name, group_settings in user_settings_f._settings_structure:
            for k, visible, _, data_type, default, __ in group_settings:
                if data_type == "boolean":
                    v = "True" if k in request.params else "False"
                else:
                    v = request.params[k]
                
                if v != str(settings_dict.get(k)):
                    user_settings_f.set_setting(request.user.id, k, v)
                    settings_dict[k] = v
        
        message = "success", "Settings succesfully changed."
    
    return dict(
        title          = "User control panel",
        layout         = layout,
        pre_content    = pre_content,
        message        = message,
        
        settings_dict  = settings_dict,
        setting_groups = user_settings_f._settings_structure,
    )

def account(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    message = None
    
    the_user = user_f.get_user(request.user.id)
    mode = request.params.get('mode', '')
    
    if mode == "password_change":
        current_password = request.params['current_password']
        password1 = request.params['new_password1']
        password2 = request.params['new_password2']
        
        if len(password1) < 8:
            raise common.GracefulException("Inadequate password", """Your password must be at least 8 characters long.""",
                category="Input")
        
        if password1 == "password":
            raise common.GracefulException("Insecure password", """You cannot change your password to "password".""",
                category="Input")
        
        if password1 != "":
            if password1 == password2:
                if the_user.test_password(current_password):
                    the_user.new_password(password1)
                    user_f.save(the_user, flush=True)
                    
                    message = "success", "Password successfully updated"
                else:
                    message = "danger", "Your current password was entered incorrectly, this may sound silly but make sure it's going into the right box (that's the mistake I always make)"
            else:
                message = "danger", "Passwords do not match"
    
    return dict(
        title                = "Account settings",
        layout               = layout,
        pre_content          = pre_content,
        message              = message,
    )

def list_groups(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    results = user_f.get_groups(request.user.id)
    
    return dict(
        title       = "User: Groups",
        layout      = layout,
        pre_content = pre_content,
        results     = results,
    )
    

def create_group(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    response = dict(
        title       = "Add group",
        layout      = layout,
        pre_content = pre_content,
        message     = None
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
        return HTTPFound(location=request.route_url('user.groups.edit', group_id=new_user.id))
    
    # response['message'] = "danger", "No username was provided"
    return response

def edit_group(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    group_id = int(request.matchdict['group_id'])
    the_group, the_owner = user_f.get_group_and_owner(group_id)
    message = None
    
    UserPicker(request)
    
    request.add_documentation("user.groups.edit_group")
    
    members = tuple(user_f.get_users(the_group.id))
    
    # Is the user a member?
    user_is_member = False
    for m in members:
        if m.id == request.user.id:
            user_is_member = True
            break
    
    if not user_is_member:
        message = "warning", "You are not a member of this group, only the owner. This means you will not count as being part of the group (though can still edit it). If you want to count as part of the group, you need to add yourself to it."
    
    try:
        admin_f.check_group_edit_permissions(request, the_group, members)
    except Exception as e:
        raise
        return HTTPFound(location=request.route_url('user.groups.view', group_id=the_group.id))
    
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
        title       = "User: Edit group",
        layout      = layout,
        pre_content = pre_content,
        the_group   = the_group,
        the_owner   = the_owner,
        message     = message,
        common      = common,
        
        members     = members,
        group_types = {k:v for k,v in enumerate(group_types)},
    )

def view_group(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    group_id = int(request.matchdict['group_id'])
    the_group, the_owner = user_f.get_group_and_owner(group_id)
    message = None
    
    members = tuple(user_f.get_users(the_group.id))
    
    try:
        admin_f.check_group_view_permissions(request, the_group, members)
    except Exception as e:
        return HTTPFound(location=request.route_url('user.groups.list'))
    
    return dict(
        title       = "User: Edit group",
        layout      = layout,
        pre_content = pre_content,
        the_group   = the_group,
        the_owner   = the_owner,
        message     = message,
        common      = common,
        
        members     = members,
        group_types = {k:v for k,v in enumerate(group_types)},
    )

def remove_group(request):
    pass

def add_member_to_group(request):
    group_id = int(request.matchdict['group_id'])
    the_group = user_f.get_user(group_id, allow_groups=True)
    members = tuple(user_f.get_users(the_group.id))
    
    admin_f.check_group_edit_permissions(request, the_group, members)
    
    usernames = (u.strip() for u in request.params['usernames'].replace(",", "\n").split("\n"))
    user_ids = user_f.get_user_ids_by_name(*usernames)
    
    member_ids = [u.id for u in members]
    ids_to_add = filter(lambda u: u not in member_ids, user_ids)
    
    user_f.add_users_to_group(group_id, *ids_to_add)
    return HTTPFound(location=request.route_url('user.groups.edit', group_id=group_id))

def remove_member_from_group(request):
    group_id = int(request.matchdict['group_id'])
    the_group = user_f.get_user(group_id, allow_groups=True)
    members = tuple(user_f.get_users(the_group.id))
    
    admin_f.check_group_edit_permissions(request, the_group, members)
    
    userids = [int(u) for u in request.params['userids'].split(",")]
    user_f.remove_users_from_group(group_id, *userids)
    
    return HTTPFound(location=request.route_url('user.groups.edit', group_id=group_id))