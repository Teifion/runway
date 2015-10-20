from sqlalchemy import func, and_
from sqlalchemy.orm import aliased
from functools import reduce
from ...system.lib import auth
from ...base import DBSession
from ...system.models.user import User, UserPermissionGroup

default_per_page = 15

def by_username(terms, page=1, per_page=default_per_page, allow_groups=False, groups_only=False):
    # This block allows us to filter on users, gropus and users and groups
    if groups_only:         group_filter = (User.group_owner != None)
    elif allow_groups:      group_filter = True
    elif not allow_groups:  group_filter = (User.group_owner == None)
    
    return _list_users([
        func.lower(User.username).like('%{}%'.format(terms.lower())),
        group_filter,
        ], page=page, per_page=default_per_page)

def by_display_name(terms, page=1, per_page=default_per_page, allow_groups=False, groups_only=False):
    # This block allows us to filter on users, gropus and users and groups
    if groups_only:         group_filter = (User.group_owner != None)
    elif allow_groups:      group_filter = True
    elif not allow_groups:  group_filter = (User.group_owner == None)
    
    return _list_users([
        func.lower(User.display_name).like('%{}%'.format(terms.lower())),
        group_filter,
        ], page=page, per_page=default_per_page)

def by_either_name(terms, page=1, per_page=default_per_page, allow_groups=False, groups_only=False):
    # This block allows us to filter on users, gropus and users and groups
    if groups_only:         group_filter = (User.group_owner != None)
    elif allow_groups:      group_filter = True
    elif not allow_groups:  group_filter = (User.group_owner == None)
    
    return _list_users(
        [
            func.lower(User.username).like('%{}%'.format(terms.lower())),
            func.lower(User.display_name).like('%{}%'.format(terms.lower())),
            group_filter,
        ],
        page=page,
        per_page=default_per_page
    )

def by_group(group_name, page=1, per_page=default_per_page):
    if isinstance(group_name, str):
        the_filter = func.lower(UserPermissionGroup.group) == group_name.lower()
    else:
        the_filter = UserPermissionGroup.group.in_(group_name)
    
    return DBSession.query(
        User,
    ).filter(
        the_filter,
        User.group_owner == None,
    ).outerjoin(
        (UserPermissionGroup, and_(UserPermissionGroup.user == User.id)),
    ).order_by(
        User.username,
    ).limit(
        per_page
    ).offset(
        per_page * (page-1)
    )

def by_permission(permission_name, page=1, per_page=default_per_page):
    # First we find out which groups have this permission
    predicate = lambda ag: permission_name in ag.permissions
    groups = [ag.name for ag in filter(predicate, auth.RootFactory.__acl__)]
    
    # No groups? No query
    if groups == []:
        return []
    
    return by_group(groups, page=page, per_page=default_per_page)

def _list_users(filters, page=1, per_page=default_per_page):
    return DBSession.query(
        User,
    ).filter(
        *filters
    ).order_by(
        User.username,
    ).limit(
        per_page
    ).offset(
        per_page * (page-1)
    )

def all_users():
    return DBSession.query(User).filter(User.id > 2).order_by(User.id.asc())

def find_groups(group_name):
    group_name = "%{}%".format(group_name)
    owner_table = aliased(User, name="owner_table")
    
    return DBSession.query(
        User,
        owner_table
    ).filter(
        User.username.like(group_name),
        User.group_owner != None,
        owner_table.id == User.group_owner
    ).order_by(
        User.username,
    )

def custom_search(filters, orders, limit=40):
    return DBSession.query(
        User
    ).filter(
        *filters
    ).order_by(
        *orders
    ).limit(
        limit
    )
