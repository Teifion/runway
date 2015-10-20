from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    String,
    Date,
    ForeignKey,
)

from pyramid.security import (
    forget,
)

from sqlalchemy import func
from sqlalchemy.orm import reconstructor
from passlib.hash import sha256_crypt
from pyramid.authentication import AuthTktCookieHelper
from pyramid.httpexceptions import HTTPFound

import string
import random

from ...base import Base, DBSession
from ..lib import auth

group_types = (
    "Anybody",
    "Members",
    "Owner",
)

class User(Base):
    __tablename__   = 'runway_users'
    id              = Column(Integer, primary_key=True)
    username        = Column(String, nullable=False, unique=True)
    display_name    = Column(String, nullable=False)
    initials        = Column(String, nullable=False, default='')
    
    email           = Column(String, nullable=False, default='')
    
    password        = Column(String, nullable=False, default='')
    
    secure_password = Column(Boolean, default=False)
    
    date_of_birth   = Column(Date, nullable=True)
    join_date       = Column(Date, nullable=True)
    
    session_ip      = Column(String, nullable=False, default='')
    remote_id       = Column(String, nullable=False, default='')
    
    group_owner     = Column(Integer, ForeignKey("runway_users.id"), nullable=True)
    
    
    
    """
    Group permission flags
    None = Not a group
    0 = Anybody (public)
    1 = Members only
    2 = Owner only
    
    Type    View    Edit
    public  0       0
    invite  1       1
    private 2       2
    """
    
    group_view = Column(Integer, nullable=True)
    group_edit = Column(Integer, nullable=True)
    
    active     = Column(Boolean, nullable=False, default=True)
    
    @reconstructor
    def init_on_load(self):
        self._permissions = None
        self._groups      = None
    
    def new_password(self, new_password):
        saltable = string.ascii_letters + string.digits
        salt = "".join([random.choice(saltable) for x in range(16)])
        self.password = sha256_crypt.encrypt(new_password, salt=salt)
    
    def test_password(self, new_password):
        return sha256_crypt.verify(new_password, self.password)
    
    def get_groups(self):
        groups = DBSession.query(UserPermissionGroup.group).filter(UserPermissionGroup.user == self.id)
        self._groups = tuple([g[0] for g in groups])
        return self._groups
    
    def permissions(self, recache=False):
        if self._permissions != None and not recache:
            return self._permissions
        
        self._permissions = []
        
        if self._groups is None:
            self.get_groups()
        
        for g in self._groups:
            self._permissions.extend(auth.group_lookup.get(g, []))
            # self._permissions.extend(auth.group_lookup[g])
            self._permissions.append(g)
        
        # self._permissions = set(self._permissions)
        self._permissions = auth.PermissionSet(self._permissions)
        return self._permissions

class UserGroupMembership(Base):
    __tablename__ = 'runway_user_group_memberships'
    user          = Column(Integer, ForeignKey("runway_users.id"), primary_key=True)
    group         = Column(Integer, ForeignKey("runway_users.id"), primary_key=True)


def add_column(name, column):
    setattr(User, name, column)

class SecurityCheck(Base):
    __tablename__ = 'runway_security_checks'
    id            = Column(Integer, primary_key=True)
    
    user          = Column(Integer, ForeignKey("runway_users.id"), primary_key=True)
    check         = Column(String, nullable=False)
    data          = Column(String, nullable=False)

class PartialLogin(Base):
    """Used to track multi-stage logins"""
    __tablename__ = 'runway_partial_login'
    user          = Column(Integer, ForeignKey("runway_users.id"), primary_key=True)
    hash          = Column(String, index=True)
    ip            = Column(String)
    
    remaining     = Column(String, nullable=False)
    data_str      = Column(String, nullable=False, default='{}')

class UserPermissionGroup(Base):
    __tablename__ = 'runway_user_permission_group_memberships'
    user          = Column(Integer, ForeignKey("runway_users.id"), primary_key=True)
    group         = Column(String, primary_key=True)


def groupfinder(user_id, request):
    if not hasattr(request, "user"):
        results = DBSession.query(
            User,
            UserPermissionGroup.group,
        ).filter(
            User.id == user_id,
            UserPermissionGroup.user == user_id,
        )
        
        # Assign the groups
        the_user = None
        groups = []
        for the_user, g in results:
            groups.append(g)
        
        if the_user is None:
            the_user = DBSession.query(User).filter(User.id == user_id).first()
        
        # Still None?
        if the_user is None:
            return []
        
        # Check auth, nobody is allowed to connect from more than
        # one IP at a time
        # if request.path != "/logout":
        #     if request.remote_addr != the_user.session_ip:
        #         if request.remote_addr != None:
        #             headers = forget(request)
        #             raise HTTPFound(request.route_url('core.login'), headers=headers)
        
        the_user._groups = groups
        
        request.user = the_user
        DBSession.expunge(the_user)
    
    return request.user.permissions() | {"loggedin"}

class UserRelationshipType(Base):
    __tablename__   = 'runway_user_relationship_types'
    id              = Column(Integer, primary_key=True)
    name            = Column(String)
    
    primary_label   = Column(String)
    secondary_label = Column(String)

class UserRelationship(Base):
    __tablename__ = 'runway_user_relationships'
    user1         = Column(Integer, ForeignKey("runway_users.id"), primary_key=True)
    user2         = Column(Integer, ForeignKey("runway_users.id"), primary_key=True)
    relationship  = Column(Integer, ForeignKey("runway_user_relationship_types.id"), primary_key=True)
