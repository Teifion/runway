from passlib.hash import sha256_crypt
from pyramid.httpexceptions import HTTPFound
import hashlib
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import label
import transaction
from datetime import date
from collections import namedtuple
from time import sleep

from ....core.documentation.lib.docs_f import document_function
from ...lib import common
from . import errors_f

from ...base import DBSession
from ..models.user import (
    User,
    UserPermissionGroup,
    UserRelationshipType,
    UserRelationship,
    UserGroupMembership,
    SecurityCheck,
    group_types,
)

# Designed to be used in a map to pull just the ids back from a query of users
ids = lambda u: u.id

def attempt_login(username, password, run_crypt=True):
    the_user = DBSession.query(
        User.id,
        User.password,
    ).filter(
        or_(
            func.lower(User.username) == username.lower(),
            func.lower(User.display_name) == username.lower(),
        )
    ).first()
    
    # No user found
    if the_user == None:
        raise Exception("Login unsuccessful")
    
    if password == "":
        raise Exception("Invalid password")
    
    # Test the password
    if run_crypt:
        try:
            if not auth(the_user.password, password):
                raise Exception("Invalid password")
        except ValueError:
            # We can get issues with invalid hashes sometimes, I have
            # a hunch it's because of empty passwords but can't be sure
            raise Exception("Invalid password")
    
    return the_user.id

def auth(user_password, entered_password):
    return sha256_crypt.verify(entered_password, user_password)

def update_session_ip(user_id, session_ip):
    with transaction.manager:
        try:
            DBSession.execute("UPDATE {table} SET session_ip = '{session_ip}' WHERE id = {user_id:d}".format(
                table      = User.__tablename__,
                session_ip = session_ip,
                user_id    = user_id,
            ))
        except Exception as e:
            sleep(0.1)
            DBSession.execute("UPDATE {table} SET session_ip = '{session_ip}' WHERE id = {user_id:d}".format(
                table      = User.__tablename__,
                session_ip = session_ip,
                user_id    = user_id,
            ))
        
        DBSession.execute("COMMIT")
        

def get_user_security_checks(user_id):
    return DBSession.query(SecurityCheck).filter(SecurityCheck.user == user_id)

def get_userid(username, allow_groups=False):
    r = DBSession.query(User.id).filter(User.username == username.strip())
    
    if not allow_groups:
        r = r.filter(User.group_owner == None)
    
    r = r.first()
    if r == None: return None
    return r[0]

def get_username(user_id, allow_groups=False):
    r = DBSession.query(User.username).filter(User.id == user_id)
    
    if not allow_groups:
        r = r.filter(User.group_owner == None)
    
    r = r.first()
    if r == None: return None
    return r[0]

def get_user(user_id, allow_groups=False):
    if user_id is None: return None
    
    if type(user_id) == str:
        filters = [User.username == user_id.strip()]
    else:
        filters = [User.id == int(user_id)]
    
    if not allow_groups:
        filters.append(User.group_owner == None)
    
    return DBSession.query(User).filter(*filters).first()

def get_group(group_id):
    if group_id is None: return None
    
    if type(group_id) == str:
        filters = [User.username == group_id.strip()]
    else:
        filters = [User.id == int(group_id)]
    
    return DBSession.query(User).filter(User.group_owner != None, *filters).first()

def find_groups(the_string, requester, just_ids=False):
    """
    Pass a string such as "group 1, group 2 & groups 3"
    
    It will break the string into chuncks (& and , are separators) and
    return a list of the groups as expected.
    """
    
    # Split and strip the results
    the_string = the_string.replace(",", "&")
    parts = [s.strip().lower() for s in the_string.split("&")]
    
    # Now pull back the parts based on permissions, also pull back the membership of
    # the requester if it's a group
    interim_results = DBSession.query(
        User,
        UserGroupMembership
    ).filter(
        User.username.in_(parts),
        User.group_owner != None,
    ).outerjoin(
        (UserGroupMembership, and_(
            UserGroupMembership.group == User.id,
            UserGroupMembership.user == requester.id
        )),
    )
    
    groups = []
    
    for user, member in interim_results:
        # User, nice and simply
        if user.group_owner == None:
            results.append(user)
        
            # More complex as it's now a group
        else:
            if user.group_view == group_types.index("Owner"):
                if user.group_owner == requester.id or 'su' in requester.permissions():
                    groups.append(user)
            
            elif user.group_view == group_types.index("Members"):
                if member != None or 'su' in requester.permissions():
                    groups.append(user)
            
            elif user.group_view == group_types.index("Anybody"):
                groups.append(user)
    
    if just_ids:
        return [g.id for g in groups]
    return groups

def search_multiuser_string(the_string, requester, just_ids=False):
    """
    Pass a string such as "root, jordant & fred123"
    
    It will break the string into chuncks (& and , are separators) and
    return a list of users listed and members of groups listed but only
    where the requester has the ability to read that group
    """
    
    # Split and strip the results
    the_string = the_string.replace(",", "&")
    parts = [s.strip().lower() for s in the_string.split("&")]
    
    # Now pull back the parts based on permissions, also pull back the membership of
    # the requester if it's a group
    interim_results = DBSession.query(
        User,
        UserGroupMembership
    ).filter(
        User.username.in_(parts)
    ).outerjoin(
        (UserGroupMembership, and_(
            UserGroupMembership.group == User.id,
            UserGroupMembership.user == requester.id
        )),
    )
    
    results = []
    groups = []
    
    for user, member in interim_results:
        # User, nice and simply
        if user.group_owner == None:
            results.append(user)
        
            # More complex as it's now a group
        else:
            if user.group_view == group_types.index("Owner"):
                if user.group_owner == requester.id or 'su' in requester.permissions():
                    groups.append(user.id)
            
            elif user.group_view == group_types.index("Members"):
                if member != None or 'su' in requester.permissions():
                    groups.append(user.id)
            
            elif user.group_view == group_types.index("Anybody"):
                groups.append(user.id)
    
    # If we have no groups, we can just return the names of the users
    # we found
    if len(groups) == 0:
        if just_ids:
            return [r.id for r in results]
        return results
    
    # Now to grab the contents of the groups
    second_results = list(DBSession.query(
        (User.id if just_ids else User)
    ).filter(
        
    ).join(
        (UserGroupMembership, and_(UserGroupMembership.group.in_(groups), User.id == UserGroupMembership.user)),
    ))
    
    # If it's just ids then we want to remove the tupleness of them
    if just_ids:
        return [r.id for r in results] + [u[0] for u in second_results]
    
    return results + second_results


def get_users(*identifiers):
    """
    This function is used to pull back either a group of users or a
    single user without specifying anything special. Groups are
    identified with a naming convention and single users will have
    only themselves as members of themselves.
    """
    
    member_table = aliased(User, name="member_table")
    group_table = aliased(User, name="group_table")
    
    if isinstance(identifiers[0], int):
        return DBSession.query(
            member_table
        ).join(
            (UserGroupMembership, and_(
                UserGroupMembership.group.in_(identifiers),
                UserGroupMembership.user == member_table.id
            )),
        ).filter(
            member_table.group_owner == None,
        )
    elif isinstance(identifiers[0], str):
        return DBSession.query(
            member_table
        ).join(
            (UserGroupMembership, and_(
                UserGroupMembership.group == group_table.id,
                UserGroupMembership.user == member_table.id
            )),
        ).filter(
            member_table.group_owner == None,
            group_table.username.in_(identifiers)
        )
    else:
        raise Exception("No handler for identifiers type of {}".format(type(identifiers[0])))

def get_user_ids_by_name(*usernames):
    usernames = [u.strip().lower() for u in usernames]
    return (u[0] for u in DBSession.query(User.id).filter(func.lower(User.username).in_(usernames)))

def get_user_and_groups(user_id):
    if user_id is None: return None
    
    if type(user_id) == str:
        filters = [User.username == user_id.strip()]
    else:
        filters = [User.id == int(user_id)]
    
    query = DBSession.query(
        User,
        UserPermissionGroup.group
    ).outerjoin(
        UserPermissionGroup, and_(UserPermissionGroup.user == User.id)
    ).filter(*filters)
    
    groups = []
    for u, g in query:
        the_user = u
        
        if g != None:
            groups.append(g)
    
    return the_user, groups

def get_groups(user_id=None):
    member_table = aliased(User, name="member_table")
    owner_table = aliased(User, name="owner_table")
    group_table = aliased(User, name="group_table")
    
    # No user id, get all the groups
    if user_id is None:
        return DBSession.query(
            group_table,
            member_table,
        ).filter(
            # group_table.group_owner == member_table.id
        ).join(
            (member_table, and_(group_table.group_owner == member_table.id)),
        ).order_by(
            group_table.username
        )
    
    # User id supplied, get the groups they are part of
    return DBSession.query(
        group_table,
        owner_table,
        UserGroupMembership,
    ).filter(
        # group_table.group_owner == member_table.id
    ).join(
        (owner_table, and_(
            group_table.group_owner == owner_table.id
        )),
    ).outerjoin(
        (UserGroupMembership, and_(
            group_table.id == UserGroupMembership.group,
            UserGroupMembership.user == user_id
        ))
    ).filter(
        or_(
            owner_table.id == user_id,
            UserGroupMembership.user == user_id
        )
    ).order_by(
        group_table.username
    )
    
def save(the_user, flush=False, return_id=False):
    try:
        DBSession.add(the_user)
        if flush: DBSession.flush()
    except Exception as e:
        print("\n\n")
        print(e.args)
        print("\n\n")
        raise e
    
    if return_id:
        return DBSession.query(
            User.id
        ).filter(
            User.username == the_user.username
        ).order_by(
            User.id.desc()
        ).first()[0]

    

def add_permission_group_membership(user_id, group_name):
    try:
        return DBSession.add(UserPermissionGroup(
            user  = user_id,
            group = group_name,
        ))
    except Exception as e:
        raise common.GracefulException(
            "Oops, something went wrong",
            "There was an error with the database. I'm not sure why this happened, at best I think it happened because the page was refreshed before expected (you've done nothing wrong). We've logged this error so there's nothing you need to do.",
            log_anyway=True
        )
    

def remove_permission_group_membership(user_id, group_name):
    return DBSession.query(UserPermissionGroup).filter(
        UserPermissionGroup.user == user_id,
        UserPermissionGroup.group == group_name,
    ).delete()

def add_security_check(user_id, check_name, data, return_id=False):
    DBSession.add(SecurityCheck(
        user  = user_id,
        data  = data,
        check = check_name,
    ))
    
    if return_id:
        return DBSession.query(
            SecurityCheck.id
        ).filter(
            SecurityCheck.user == user_id
        ).order_by(
            SecurityCheck.id.desc()
        ).first()[0]

def remove_security_check(check_id):
    return DBSession.query(SecurityCheck).filter(
        SecurityCheck.id == check_id,
    ).delete()

def make_username(actual_name):
    """Designed to be overriden based on your system's rules"""
    names = actual_name.strip().split(" ")
    firstname = names[0]
    surname = names[-1]
    
    # First 8 letters of your firstname plus the first letter of your surname
    return (firstname[:8] + surname[0]).lower()

def blank_user():
    """Creates a blank user"""
    the_user = User()
    the_user.username = "username"
    the_user.display_name = "display_name"
    
    # Defaults the password to 'password'
    # you should use the User.new_password() function
    # to generate a secure password if you want it to be secure
    the_user.password = '$5$rounds=110000$A1vz94RZAKWk6mzf$mqMkuKbzKrNOddYhVnnElAPG0KQImtds6kQX1iSThf6'
    the_user.secure_password = False
    the_user.join_date = date.today()
    
    return the_user


def get_group_and_owner(group_id):
    group_table = aliased(User, name="group_table")
    owner_table = aliased(User, name="owner_table")
    
    return DBSession.query(
        group_table,
        owner_table,
    ).filter(
        group_table.id == group_id
    ).join(
        (owner_table, and_(group_table.group_owner == owner_table.id)),
    ).first()

def add_users_to_group(group_id, *user_ids):
    users = ["({}, {})".format(user_id, group_id) for user_id in user_ids]
    
    if len(users) > 0:
        with transaction.manager:
            DBSession.execute("""INSERT INTO {table} ("user", "group") VALUES {values}""".format(
                table = UserGroupMembership.__tablename__,
                values = ",".join(users),
            ))
            DBSession.execute("""COMMIT""")

def remove_users_from_group(group_id, *user_ids):
    DBSession.query(
        UserGroupMembership
    ).filter(
        UserGroupMembership.group == group_id,
        UserGroupMembership.user.in_(user_ids)
    ).delete(synchronize_session='fetch')

def get_relationship_types():
    return DBSession.query(UserRelationshipType).order_by(UserRelationshipType.name.asc())

def add_relationship_type(the_type):
    DBSession.add(the_type)

def remove_relationship_type(type_id):
    DBSession.query(UserRelationshipType).filter(UserRelationshipType.id == type_id).delete()

def get_relationships(user_id, relationship_type=None):
    user_1_table = aliased(User, name="user_1_table")
    user_2_table = aliased(User, name="user_2_table")
    
    return DBSession.query(
        UserRelationshipType,
        user_1_table,
        user_2_table,
    ).filter(
        or_(user_1_table.id == user_id, user_2_table.id == user_id),
    ).join(
        (UserRelationship, and_(UserRelationship.relationship == UserRelationshipType.id)),
        (user_1_table, and_(user_1_table.id == UserRelationship.user1)),
        (user_2_table, and_(user_2_table.id == UserRelationship.user2)),
    )

def add_relationship(relationship, user1, user2):
    # First try deleteing this relationship to ensure it doesn't already exist
    remove_relationship(relationship, user1, user2)
    return DBSession.add(UserRelationship(
        user1             = user1,
        user2             = user2,
        relationship = relationship,
    ))

def remove_relationship(relationship, user1, user2):
    return DBSession.query(UserRelationship).filter(
        or_(
            and_(UserRelationship.user1 == user1, UserRelationship.user2 == user2),
            and_(UserRelationship.user1 == user2, UserRelationship.user2 == user1),
        ),
        UserRelationship.relationship == relationship,
    ).delete()

# def require_secure_password(request, action="error"):
#     if request.user.secure_password:
#         return True
    
#     if action == "error":
#         raise errors_f.GracefulException("Insecure password", """You cannot access this section with an insecure password. Please change your password in the User control panel to proceed.
#             <br /><br />.
#             <a href="{}" class="btn btn-default">Dashboard home</a>
#             <a href="{}" class="btn btn-default">User control panel</a>
#             """.format(
#                 request.route_url('/'),
#                 request.route_url('user_cp'),
#         ), category="Password")
    
#     if action[0:8] == "forward:":
#         try:
#             location = request.route_url(action.replace('forward:', ''))
#         except Exception:
#             location = request.route_url('/')
        
#         raise HTTPFound(location = location)
    
#     raise Exception("Insecure password")

signthrough_form_html = """
<form action="?" method="post">
  <input type="password" name="agent_password" id="agent_password" value="" placeholder="Enter agent ({agent_name}) pasword to confirm feedback was given" class="form-control" autofocus="autofocus"/>
  <br />
  
  <input type="submit" value="Submit" name="form.submitted" class="btn btn-primary pull-right" />
</form>
"""

def build_signthrough(agent_name):
    return signthrough_form_html.format(agent_name=agent_name)

def add_user(the_user, return_id=False):
    """
    Docstring
    """
    DBSession.add(the_user)
    
    if return_id:
        DBSession.flush()
        user_id = DBSession.query(User.id).filter(User.username == the_user.username).order_by(User.id.desc()).first()
        
        if user_id is None: return None
        return user_id[0]

# WIP, not used yet
def document_functions():
    pass
    # document_function(__file__, add_user)
