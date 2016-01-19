from pyramid.httpexceptions import HTTPFound
from ...base import DBSession
from ...system.models.user import (
    User,
    UserGroupMembership,
    group_types,
)
from ...system.lib import auth, user_f
from sqlalchemy import and_, or_
from ...lib import funcs
from ...plugins.lib import plugins_f
from functools import reduce
from sqlalchemy.orm import aliased
from functools import lru_cache
from datetime import date
import os
import warnings

def admin_user_permissions(the_admin, the_user, the_user_groups):
    # Root can do anything, even edit themselves
    if the_admin.id == 1:
        return ['view', 'edit']
    
    # You can't edit yourself or a super user
    if "su" in the_user_groups or the_admin.id == the_user.id:
        return ['view']
    
    # If you are a developer you can do anything
    if "su" in the_admin._groups:
        return ['view', 'edit']
    
    # Are you as high a rank as this person?
    the_admin_rank = max(map(
        lambda g: auth.ag_lookup[g].kwargs.get('admin_rank', -1),
        the_admin.get_groups()
    ))
    
    if the_user_groups != []:
        the_user_rank = max(map(
            lambda g: auth.ag_lookup[g].kwargs.get('admin_rank', -1),
            the_user_groups,
        ))
    else:
        the_user_rank = -1
    
    if the_admin_rank <= the_user_rank:
        return ['view']
    
    # Assume you can edit and view
    return ['view', 'edit']
    
def check_user_edit_permissions(request, the_user, the_user_groups):
    permissions = admin_user_permissions(request.user, the_user, the_user_groups)
    
    if "edit" not in permissions:
        raise HTTPFound(request.route_url('admin.user.view', user_id=the_user.id))

def check_user_view_permissions(request, the_user, the_user_groups):
    permissions = admin_user_permissions(request.user, the_user, the_user_groups)
    
    if "view" not in permissions:
        raise HTTPFound(request.route_url('admin.home'))


def admin_group_permissions(the_admin, the_group, members):
    # Root can do anything, even edit themselves
    if the_admin.id == 1:
        return ['view', 'edit']
    
    # If you are a super user you can do anything, or if you own the group
    if "su" in the_admin._groups or the_group.group_owner == the_admin.id:
        return ['view', 'edit']
    
    # Editing
    if the_group.group_edit == group_types.index("Owner"):
        edit = (the_group.group_owner == the_admin.id)
    elif the_group.group_edit == group_types.index("Members"):
        edit = the_admin.id in members
    elif the_group.group_edit == group_types.index("Anybody"):
        edit = True
    else:
        raise Exception("No handler for group_edit of '{}'. Group ID = {}".format(the_group.group_edit, the_group.id))
    
    # Viewing
    if the_group.group_view == group_types.index("Owner"):
        view = (the_group.group_owner == the_admin.id)
    elif the_group.group_view == group_types.index("Members"):
        view = the_admin.id in members
    elif the_group.group_view == group_types.index("Anybody"):
        view = True
    else:
        raise Exception("No handler for group_view of '{}'. Group ID = {}".format(the_group.group_view, the_group.id))
    
    # If the admin can edit users they can at least view this
    if "admin.user.edit" in the_admin._groups:
        view = True
    
    result = []
    if edit: result.append('edit')
    if view: result.append('view')
    
    return result

def check_group_edit_permissions(request, the_group, members):
    if len(members) > 0:
        if isinstance(members[0], User):
            members = [m.id for m in members]
        elif isinstance(members[0], tuple):
            members = [m[0] for m in members]
    
    permissions = admin_group_permissions(request.user, the_group, members)
    
    if "edit" not in permissions:
        raise HTTPFound(request.route_url('admin.groups.view', group_id=the_group.id))

def check_group_view_permissions(request, the_group, members):
    if len(members) > 0:
        if isinstance(members[0], User):
            members = [m.id for m in members]
        elif isinstance(members[0], tuple):
            members = [m[0] for m in members]
    
    permissions = admin_group_permissions(request.user, the_group, members)
    
    if "view" not in permissions:
        raise HTTPFound(request.route_url('admin.home'))

def get_user_groups(user_id):
    owner_table = aliased(User, name="owner_table")
    group_table = aliased(User, name="group_table")
    
    return DBSession.query(
        group_table,
        owner_table,
    ).outerjoin(
        (UserGroupMembership, and_(
            UserGroupMembership.group == group_table.id,
            UserGroupMembership.user == user_id
        ))
    ).join(
        (owner_table, and_(owner_table.id == group_table.group_owner))
    ).filter(
        or_(
            UserGroupMembership.user != None,
            group_table.group_owner == user_id
        )
    )


def get_admin_rank(user_groups):
    if len(user_groups) == 0:
        return 0
    
    if len(user_groups) == 1:
        return auth.ag_lookup[user_groups[0]].kwargs.get('admin_rank', 0)
    
    return reduce(
        lambda a, b: max(a.kwargs.get('admin_rank',0), b.kwargs.get('admin_rank',0)),
        (auth.ag_lookup[g] for g in user_groups),
    )

def get_editable_groups(user_groups):
    admin_rank = get_admin_rank(user_groups)
    
    return filter(
        lambda ag: ag.rank < admin_rank and not ag.kwargs.get('system_only', False),
        auth.ag_lookup.values(),
    )

def mass_add(user_data, commit=False):
    col_count = len(user_data[0].split("\t"))
    
    if col_count == 1: creator_function = _mass_add_1
    else: raise Exception("No handler for a column count of {}".format(col_count))
    
    # Get existing usernames
    existing_usernames = {n[0] for n in DBSession.query(User.username)}
    new_users = []
    
    # Ignore empty lines, strip stuff
    predicate = lambda v: v.strip() != ""
    mapper = lambda v: v.strip()
    
    for row in map(mapper, filter(predicate, user_data)):
        u = creator_function(row.strip())
        
        # Now we want to ensure we've not duplicated the username
        if u.username in existing_usernames:
            suffix = 1
            while u.username + str(suffix) in existing_usernames:
                suffix += 1
            
            u.username = u.username + str(suffix)
        
        new_users.append(u)
        existing_usernames.add(u.username)
    
    if commit:
        for u in new_users:
            DBSession.add(u)
    
    DBSession.flush()
    return new_users

def _mass_add_1(row):
    the_user = user_f.blank_user()
    
    the_user.username = user_f.make_username(row)
    the_user.display_name = row.title()
    
    return the_user

def new_username(display_name):
    # First find out what the username base is
    username = user_f.make_username(display_name)
    
    stmt = """SELECT username
        FROM runway_users
        WHERE "username" SIMILAR TO :username
    """
    
    args = {"username":username + r"[0-9]*"}
    
    existing_usernames = {r[0] for r in DBSession.execute(stmt, args)}
    
    '''
    # Now find all the usernames this collides with
    the_filter = """ "username" SIMILAR TO '{}' """.format(username + r'[0-9]*')
    
    # Dev mode has warnings on, this above query can generate
    # an SQL warning which we want to ignore
    # The warning generated is:
    # 
    # Textual SQL expression ' "username" SIMILAR TO \'1...' should be explicitly declared as text(' "username" SIMILAR TO \'1...') (this warning may be suppressed after 10 occurrences)
    # 
    existing_warnings = list(warnings.filters)
    warnings.resetwarnings()
    
    existing_usernames = {n[0] for n in DBSession.query(User.username).filter(the_filter)}
    
    # Now we revert our change
    warnings.filters = existing_warnings
    '''
    
    if username not in existing_usernames:
        return username
    
    suffix = 1
    while username + str(suffix) in existing_usernames:
        suffix += 1
    
    return username + str(suffix)

def new_initials(display_name):
    """
    Takes a display name and returns the initials of the name
    while maintaing the case
    """
    parts = display_name.strip().replace("  ", "").split(" ")
    result = [p[0] for p in parts]
    return "".join(result).replace(" ", "")

def new_groupname(display_name):
    groupname = display_name.strip().replace(" ", "").lower()
    return groupname

def blank_group():
    """Creates a blank group, similar to user_f.blank_user()"""
    the_group = User()
    the_group.username = "groupname"
    the_group.display_name = "display_name"
    
    # Defaults the password to 'password'
    # you should use the User.new_password() function
    # to generate a secure password if you want it to be secure
    the_group.password = ''
    the_group.secure_password = False
    the_group.join_date = date.today()
    
    # Default to memeber view and owner manage
    the_group.group_view = group_types.index("Members")
    the_group.group_edit = group_types.index("Owner")
    
    the_group.group_owner = 2
    
    return the_group

@lru_cache(maxsize=1)
def get_admin_menu():
    menu = []
    
    from .. import admin_menu
    menu.extend(admin_menu)
    
    for p in plugins_f.plugins:
        if hasattr(p, "admin_menu"):
            menu.extend(p.admin_menu)
    
    section_dict = {v[2]:v for v in menu}
    section_keys = list(section_dict.keys())
    section_keys.sort()
    
    menu = [section_dict[k] for k in section_keys]
    return menu
