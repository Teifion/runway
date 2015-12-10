from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.response import Response
import io
import csv

from ..lib import searches, admin_f
from ...system.lib import user_f, auth, security
from ...lib import common
from ...system.models.user import User, UserRelationshipType
from ....core.system.js_widgets import GroupPicker

from ....core.commands import execute_command

from datetime import date

def search_username(request):
    layout      = common.render("viewer")
    
    page = int(request.params.get('page', 1))
    
    results = []
    if "username" in request.params:
        results = tuple(searches.by_username(request.params['username'], page=page))
    
    if len(results) == 1 and 'page' not in request.params:
        return HTTPFound(location=request.route_url('admin.user.edit', user_id=results[0].id))
    
    return dict(
        title       = "Admin: Search by username",
        layout      = layout,
        results     = results,
        page        = page,
    )

def search_display_name(request):
    layout      = common.render("viewer")
    
    page = int(request.params.get('page', 1))
    
    results = []
    if "display_name" in request.params:
        results = tuple(searches.by_display_name(request.params['display_name'], page=page))
    
    if len(results) == 1 and 'page' not in request.params:
        return HTTPFound(location=request.route_url('admin.user.edit', user_id=results[0].id))
    
    return dict(
        title       = "Admin: Search by display name",
        layout      = layout,
        results     = results,
        page        = page,
    )

def search_group(request):
    layout      = common.render("viewer")
    
    page = int(request.params.get('page', 1))
    
    results = []
    if "group" in request.params:
        results = tuple(searches.by_group(request.params['group'], page=page))
    
    if len(results) == 1 and 'page' not in request.params:
        return HTTPFound(location=request.route_url('admin.user.edit', user_id=results[0].id))
    
    return dict(
        title       = "Admin: Search by group",
        layout      = layout,
        results     = results,
        page        = page,
    )

def search_permission(request):
    layout      = common.render("viewer")
    
    page = int(request.params.get('page', 1))
    
    results = []
    if "group_name" in request.params:
        results = tuple(searches.by_permission(request.params['group_name'], page=page))
    
    if len(results) == 1 and 'page' not in request.params:
        return HTTPFound(location=request.route_url('admin.user.edit', user_id=results[0].id))
    
    return dict(
        title       = "Admin: Search by permission",
        layout      = layout,
        results     = results,
        page        = page,
    )

def list_users(request):
    layout      = common.render("viewer")
    
    mode = request.params.get("mode", "latest")
    
    if mode == "latest":
        results = searches.custom_search(
            filters = [User.group_owner == None],
            orders = [User.id.desc()]
        )
        
    else:
        raise KeyError("No handler for mode of {}".format(mode))
    
    return dict(
        title       = "Admin: Search by permission",
        layout      = layout,
        results     = results,
        mode        = mode,
    )

def edit(request):
    layout      = common.render("viewer")
    
    user_id = int(request.matchdict['user_id'])
    the_user, permission_groups = user_f.get_user_and_groups(user_id)
    message = None
    
    if the_user.group_owner != None:
        return HTTPFound(request.route_url("admin.groups.edit", group_id=user_id))
    
    user_relationships = user_f.get_relationships(user_id)
    
    admin_f.check_user_edit_permissions(request, the_user, permission_groups)
    
    if 'username' in request.params:
        # New username? Better check it's not taken
        new_username = request.params['username'].strip().lower()
        if new_username != the_user.username and user_f.get_userid(new_username) != None:
            message = "danger", "There is already a user with that username, no changes have been saved"
            
        else:
            the_user.username = new_username
            the_user.display_name = request.params['display_name']
            the_user.initials = request.params['initials'].strip()[0:4]
            the_user.email = request.params['email']
            
            the_user.join_date = common.string_to_datetime(request.params['join_date'])
            the_user.date_of_birth = common.string_to_datetime(request.params['date_of_birth'])
            
            password1 = request.params['password1']
            password2 = request.params['password2']
            
            if password1 != "":
                if password1 == password2:
                    the_user.new_password(password1)
                    the_user.secure_password = True
                else:
                    message = "danger", "Passwords do not match"
        
        if message == None:
            message = "success", "Changes saved"
            user_f.save(the_user)
    
    # admin_rank = admin_f.get_admin_rank(request.user._groups)
    editable_groups = admin_f.get_editable_groups(request.user._groups)
    addable_user_groups = filter(lambda v: v.name not in permission_groups, editable_groups)
    
    relationship_options = {}
    for rtype in user_f.get_relationship_types():
        relationship_options["{},primary".format(rtype.id)] = rtype.primary_label
        relationship_options["{},secondary".format(rtype.id)] = rtype.secondary_label
    
    security_check_names = {cname:sc.label for cname, sc in security.checks.items()}
    
    # Grab the user created groups they are a part of
    user_groups = admin_f.get_user_groups(user_id)
    
    return dict(
        title                = "Admin: Edit user",
        layout               = layout,
        pre_content          = pre_content,
        the_user             = the_user,
        message              = message,
        common               = common,
        
        permission_groups    = permission_groups,
        
        # Usergroups
        user_groups          = user_groups,
        
        ag_lookup            = auth.ag_lookup,
        addable_user_groups  = {ag.name:ag.label for ag in addable_user_groups},
        user_security_checks = user_f.get_user_security_checks(the_user.id),
        security_checks      = security.checks,
        security_check_names = security_check_names,
        
        user_relationships   = user_relationships,
        relationship_options = relationship_options,
    )

def view(request):
    layout      = common.render("viewer")
    
    user_id = int(request.matchdict['user_id'])
    the_user, user_groups = user_f.get_user_and_groups(user_id)
    message = None
    
    if the_user.group_owner != None:
        return HTTPFound(request.route_url("admin.groups.view", group_id=user_id))
    
    user_relationships = user_f.get_relationships(user_id)
    admin_f.check_user_view_permissions(request, the_user, user_groups)
    
    return dict(
        title            = "Admin: View user",
        layout           = layout,
        pre_content      = pre_content,
        the_user         = the_user,
        user_groups      = user_groups,
        message          = message,
        auth             = auth,
        common           = common,
        
        user_relationships = user_relationships,
    )

def mass_add(request):
    layout      = common.render("viewer")
    
    message = None
    new_users = []
    
    mode = "usernames"
    
    GroupPicker(request)
    request.add_documentation("admin.adding_users")
    
    if "groups" in request.params:
        mode = "finished"
        
        user_ids = tuple(user_f.get_user_ids_by_name(*request.params['user_data'].split("\n")))
        
        groups = user_f.find_groups(request.params['groups'], request.user)
        groups = [g.id for g in groups if g.group_owner != None]
        
        for g in groups:
            user_f.add_users_to_group(g, *user_ids)
    
    elif "confirm" in request.params:
        mode = "groups"
        new_users = admin_f.mass_add(request.params['user_data'].split("\n"), commit=True)
    
    elif 'user_data' in request.params:
        mode = "confirm"
        new_users = admin_f.mass_add(request.params['user_data'].split("\n"))
    
    return dict(
        title       = "Admin: Add users",
        layout      = layout,
        
        new_users   = new_users,
        message     = message,
        
        mode        = mode,
    )

def quick_add(request):
    layout      = common.render("viewer")
    
    response = dict(
        title       = "Admin: Quick add user",
        layout      = layout,
    )
    
    if "username" in request.params:
        the_user = user_f.blank_user()
        the_user.display_name = request.params["username"].strip()
        the_user.username = admin_f.new_username(the_user.display_name)
        the_user.initials = admin_f.new_initials(the_user.display_name)
        
        if the_user.username == "":
            response['message'] = "danger", "No username was provided"
            return response
        
        try:
            user_f.save(the_user, flush=True)
        except Exception as e:
            if e.args[0][:33] == "(UniqueError) duplicate key value":
                response['message'] = "danger", "That username already exists"
                return response
            
            raise
        
        # Now get the latest user
        new_user = user_f.get_user(the_user.username)
        return HTTPFound(location=request.route_url('admin.user.edit', user_id=new_user.id))
    
    response['message'] = "danger", "No username was provided"
    return response

    
def add_permission_group_membership(request):
    user_id    = int(request.params['user_id'])
    group_name = request.params['group']
    
    if group_name in auth.group_lookup:
        user_f.add_permission_group_membership(user_id, group_name)
    else:
        raise Exception("No group by that name (%s)" % group_name)
    
    return HTTPFound(request.route_url('admin.user.edit', user_id=user_id))

def remove_permission_group_membership(request):
    user_id    = int(request.params['user_id'])
    group_name = request.params['group']
    
    user_f.remove_permission_group_membership(user_id, group_name)
    
    return HTTPFound(request.route_url('admin.user.edit', user_id=user_id))


def add_security_check(request):
    user_id    = int(request.params['user_id'])
    check_name = request.params['check']
    data       = request.params['data'].strip()
    
    if check_name in security.checks:
        user_f.add_security_check(user_id, check_name, data)
    else:
        raise Exception("No check by that name (%s)" % check_name)
    
    return HTTPFound(request.route_url('admin.user.edit', user_id=user_id))

def remove_security_check(request):
    check_id = int(request.params['check_id'])
    user_id  = int(request.params['user_id'])
    
    user_f.remove_security_check(check_id)
    
    return HTTPFound(request.route_url('admin.user.edit', user_id=user_id))

def export(request):
    f = io.StringIO()
    w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    headers = ('id', 'username', 'display_name')
    w.writerow(headers)
    
    for the_user in searches.all_users():
        w.writerow((
            the_user.id,
            the_user.username,
            the_user.display_name,
        ))
    
    f.seek(0)
    return Response(body=f.read(), content_type='text/plain', content_disposition='attachment; filename="user_data.csv"')
    
    return f.read()


def add_relationship(request):
    target_id = user_f.get_userid(request.params['target'])
    user1 = int(request.params['user1'])
    
    # Now get the name info of the relationship
    relationship, primary = request.params['relationship'].split(",")
    primary = True if primary == 'primary' else False
    
    # Which way round is this relationship?
    if primary:
        user_f.add_relationship(int(relationship), user1, target_id)
        
    else:
        user_f.add_relationship(int(relationship), target_id, user1)
    
    return HTTPFound(request.route_url('admin.user.edit', user_id=user1))

def remove_relationship(request):
    user1     = int(request.params['user1'])
    user2     = int(request.params['user2'])
    edit_user = int(request.params['edit_user'])
    
    relationship = request.params['relationship']
    user_f.remove_relationship(int(relationship), user1, user2)
    
    return HTTPFound(request.route_url('admin.user.edit', user_id=edit_user))

def list_relationship_types(request):
    layout      = common.render("viewer")
    
    relationship_types = user_f.get_relationship_types()
    
    return dict(
        title              = "Admin: Relationship types",
        layout             = layout,
        pre_content        = pre_content,
        
        relationship_types = relationship_types,
    )

def add_relationship_type(request):
    new_type = UserRelationshipType(
        name = request.params['name'],
        primary_label = request.params['primary_label'],
        secondary_label = request.params['secondary_label'],
    )
    user_f.add_relationship_type(new_type)
    
    return HTTPFound(request.route_url('admin.user.list_relationship_types'))

def edit_relationship_type(request):
    layout      = common.render("viewer")
    
    return dict(
        title       = "Admin: Search by username",
        layout      = layout,
    )

def remove_relationship_type(request):
    type_id = int(request.matchdict['type_id'])
    user_f.remove_relationship_type(type_id)
    
    return HTTPFound(request.route_url('admin.user.list_relationship_types'))

def activate(request):
    user_id = int(request.matchdict['user_id'])
    the_user, permission_groups = user_f.get_user_and_groups(user_id)
    message = None
    
    if the_user.group_owner != None:
        return HTTPFound(request.route_url("admin.groups.edit", group_id=user_id))
    
    user_relationships = user_f.get_relationships(user_id)
    
    admin_f.check_user_edit_permissions(request, the_user, permission_groups)
    execute_command("activate_user", the_user.id)
    return HTTPFound(request.route_url('admin.user.edit', user_id=user_id))

def deactivate(request):
    user_id = int(request.matchdict['user_id'])
    the_user, permission_groups = user_f.get_user_and_groups(user_id)
    message = None
    
    if the_user.group_owner != None:
        return HTTPFound(request.route_url("admin.groups.edit", group_id=user_id))
    
    user_relationships = user_f.get_relationships(user_id)
    
    admin_f.check_user_edit_permissions(request, the_user, permission_groups)
    execute_command("deactivate_user", the_user.id)
    return HTTPFound(request.route_url('admin.user.edit', user_id=user_id))
