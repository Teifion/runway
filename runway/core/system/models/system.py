from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    Float,
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

class Schema(Base):
    __tablename__ = 'runway_schemas'
    module        = Column(String, nullable=False, primary_key=True)
    version       = Column(Float, nullable=False)
