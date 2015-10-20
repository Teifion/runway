from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    Float,
    String,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import ARRAY

from ...core.base import Base

class Category(Base):
    __tablename__     = 'tags_categories'
    id                = Column(Integer, primary_key=True)
    
    name              = Column(String, nullable=False)
    description       = Column(String, nullable=False)
    owner             = Column(Integer, ForeignKey("runway_users.id"), nullable=False)
    
    view_permissions  = Column(String, nullable=False)
    write_permissions = Column(String, nullable=False)

class Tag(Base):
    __tablename__ = 'tags_tags'
    id            = Column(Integer, primary_key=True)
    
    name          = Column(String, nullable=False)
    description   = Column(String, nullable=False)
    category      = Column(Integer, ForeignKey("tags_categories.id"), primary_key=True)
    
    primary       = Column(String, nullable=False)
    secondary     = Column(String, nullable=False)
    
# class UserTag(Base):
#     __tablename__ = 'guardian_tag_types'
#     id            = Column(Integer, primary_key=True)
#     category      = Column(Integer, ForeignKey("guardian_tag_categories.id"))
    
#     # Allows us to make users tags so you can tag an actual user
#     user         = Column(Integer, ForeignKey("runway_users.id"), nullable=True)
