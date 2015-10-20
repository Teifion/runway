from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    Float,
    Text,
    String,
    DateTime,
    
    ForeignKey,
)

from ...base import Base

class APIKey(Base):
    __tablename__ = 'runway_api_keys'
    id            = Column(Integer, primary_key=True)
    user          = Column(Integer, ForeignKey("runway_users.id"), nullable=True)
    key           = Column(String, nullable=False)
