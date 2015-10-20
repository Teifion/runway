from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    Float,
    String,
    Text,
    DateTime,
    Date,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import ARRAY

from ...base import Base, DBSession

class Setting(Base):
    __tablename__ = 'runway_settings'
    name          = Column(String, nullable=False, primary_key=True)
    value         = Column(String, nullable=False)

class UserSetting(Base):
    __tablename__ = 'runway_user_settings'
    user          = Column(Integer, ForeignKey("runway_users.id"), primary_key=True)
    name          = Column(String, primary_key=True)
    value         = Column(String, nullable=False)

class ViewLog(Base):
    __tablename__ = 'runway_logs'
    id           = Column(Integer, primary_key=True)
    user         = Column(Integer, ForeignKey("runway_users.id"), nullable=True)
    
    section      = Column(String, nullable=False, default="")
    path         = Column(String, nullable=False, default="")
    
    timestamp    = Column(DateTime)
    load_time    = Column(Float)
    
    ip           = Column(String, nullable=False, default="")

class LogAggregate(Base):
    __tablename__ = 'runway_log_aggregate'
    date          = Column(Date, primary_key=True)
    section       = Column(String, primary_key=True)
    
    page_views    = Column(ARRAY(Integer))
    unique_users  = Column(ARRAY(Integer))
    load_times    = Column(ARRAY(Float))

class ExceptionLog(Base):
    __tablename__ = 'runway_exceptions'
    id          = Column(Integer, primary_key=True)
    timestamp   = Column(DateTime)
    path        = Column(String)
    
    user        = Column(Integer, ForeignKey("runway_users.id"), nullable=True)
    assigned    = Column(Integer, ForeignKey("runway_users.id"), nullable=True)
    description = Column(String)
    traceback   = Column(Text)
    hidden      = Column(Boolean)
    
    data        = Column(Text)
