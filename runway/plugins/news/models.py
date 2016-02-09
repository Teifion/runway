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

class NewsChannel(Base):
    __tablename__ = 'news_channels'
    id            = Column(Integer, primary_key=True)
    
    # A hidden name viewable only by the system
    # this allows for "official" channels to be created
    #  by various plugins
    sys_name      = Column(String, default="")
    
    name          = Column(String, default="")
    description   = Column(String, default="")
    permissions   = Column(String, default="")
    
    owner         = Column(Integer, ForeignKey("runway_users.id"), nullable=False)

class NewsItem(Base):
    __tablename__ = 'news_items'
    id            = Column(Integer, primary_key=True)
    
    channel       = Column(Integer, ForeignKey("news_channels.id"), nullable=False)
    name          = Column(String, nullable=False)
    icon          = Column(String, nullable=False)
    content       = Column(String, nullable=False)
    
    poster        = Column(Integer, ForeignKey("runway_users.id"), nullable=False)
    timestamp     = Column(DateTime, nullable=False)
