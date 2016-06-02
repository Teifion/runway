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

class Channel(Base):
    __tablename__ = 'news_channels'
    id            = Column(Integer, primary_key=True)
    
    # A hidden name viewable only by the system
    # this allows for "official" channels to be created
    #  by various plugins
    sys_name      = Column(String, default="")
    
    name          = Column(String, default="")
    description   = Column(String, default="")
    permissions   = Column(String, default="")
    
    hidden        = Column(Boolean, default=False)
    owner         = Column(Integer, ForeignKey("runway_users.id"), nullable=False)

class Subscription(Base):
    __tablename__ = 'news_subscriptions'
    
    user    = Column(Integer, ForeignKey("runway_users.id"), nullable=False, primary_key=True)
    channel = Column(Integer, ForeignKey("news_channels.id"), nullable=False, primary_key=True)

class Item(Base):
    __tablename__ = 'news_items'
    id            = Column(Integer, primary_key=True)
    
    channel       = Column(Integer, ForeignKey("news_channels.id"), nullable=False)
    title         = Column(String, nullable=False)
    icon          = Column(String, nullable=False)
    content       = Column(String, nullable=False)
    
    poster        = Column(Integer, ForeignKey("runway_users.id"), nullable=False)
    timestamp     = Column(DateTime, nullable=True)
    
    hidden        = Column(Boolean, default=False)

class ItemTag(Base):
    __tablename__ = 'news_item_tags'
    # id            = Column(Integer, primary_key=True)
    
    item          = Column(Integer, ForeignKey("news_items.id"), nullable=False, primary_key=True)
    text          = Column(String, nullable=False, index=True, primary_key=True)

class ItemLog(Base):
    __tablename__ = 'news_item_logs'
    # id            = Column(Integer, primary_key=True)
    
    user          = Column(Integer, ForeignKey("runway_users.id"), nullable=False, primary_key=True)
    item          = Column(Integer, ForeignKey("news_items.id"), nullable=False, primary_key=True)
    
    # If invited is Null then they were not subscribed/invited to read it
    invited       = Column(DateTime, nullable=True)
    viewed        = Column(DateTime, nullable=True)
    signed        = Column(DateTime, nullable=True)
