import transaction
from sqlalchemy import func
from ...base import (
    DBSession,
    Base
)
from datetime import date
from ..models.user import (
    User,
    UserPermissionGroup,
    UserRelationshipType,
    UserRelationship,
)

from . import site_settings_f

def install_users():
    root_user = DBSession.query(User.id).filter(User.id == 1).first()
    guest_user = DBSession.query(User.id).filter(User.id == 2).first()
    
    if root_user is None:
        with transaction.manager:
            root_user = User(
                username        = 'root',
                display_name    = 'Root',
                email           = '',
                password        = '',
                secure_password = False,
                join_date       = date.today(),
                session_ip      = '',
                remote_id       = '',
            )
            root_user.new_password('password')
            
            DBSession.add(root_user)
        
        with transaction.manager:
            DBSession.query("UPDATE runway_users SET id = 1 WHERE username = 'root'")
            DBSession.query("COMMIT")
    
    if guest_user is None:
        with transaction.manager:
            guest_user = User(
                username        = 'guest',
                display_name    = 'Guest',
                email           = '',
                password        = 'This is an invalid password',
                secure_password = False,
                join_date       = date.today(),
                session_ip      = '',
                remote_id       = '',
            )
            
            DBSession.add(guest_user)
        
        with transaction.manager:
            DBSession.query("UPDATE runway_users SET id = 2 WHERE username = 'guest'")
            DBSession.query("COMMIT")

def install_groups():
    root_is_dev = DBSession.query(UserPermissionGroup).filter(
        UserPermissionGroup.user == 1,
        UserPermissionGroup.group == 'developer'
    ).first()
    
    if root_is_dev is None:
        with transaction.manager:
            DBSession.add(UserPermissionGroup(
                user = 1,
                group = 'developer',
            ))

def install_relationships():
    manager_relationship = DBSession.query(UserRelationshipType).filter(UserRelationshipType.name == 'Manager').first()
    
    if manager_relationship is None:
        with transaction.manager:
            DBSession.add(UserRelationshipType(
                name = 'Manager',
                primary_label = 'manages',
                secondary_label = 'is managed by',
            ))
        
        with transaction.manager:
            DBSession.query("""UPDATE runway_user_relationship_types SET id = 1 WHERE "name" = 'Manager'""")
            DBSession.query("COMMIT")
    
    root_manages_guest = DBSession.query(UserRelationship).filter(
        UserRelationship.user1 == 1,
        UserRelationship.user2 == 2,
        UserRelationship.relationship == 1
    ).first()
    
    if root_manages_guest is None:
        with transaction.manager:
            DBSession.add(UserRelationship(
                user1 = 1,
                user2 = 2,
                relationship = 1
            ))

def install_settings():
    from ... import (
        system,
        themes
    )
    modules = (system, themes)
    values = {}
    
    for m in modules:
        values.update(get_module_settings(m))
    
    with transaction.manager:
        site_settings_f.install_settings(values)

def get_module_settings(the_module):
    results = {}
    
    if hasattr(the_module, 'site_settings'):
        for _, setting_list in the_module.site_settings:
            for name, _, _, _, default, _ in setting_list:
                results[name] = default
    
    return results

def system_install():
    install_users()
    install_groups()
    install_relationships()
    install_settings()
    
    from ...cron.lib.installer import install_jobs as cron_install
    cron_install()

def create_tables():
    engine = DBSession.get_bind()
    Base.metadata.create_all(engine)
