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

# class TName(Base):
#     __tablename__ = ''
#     id            = Column(Integer, primary_key=True)
    
#     fkey          = Column(Integer, ForeignKey("call_audit_forms.id"), nullable=False, index=True)
#     field         = Column(DateTime, nullable=True)

class Theme(object):
    """docstring for Theme"""
    def __init__(self, arg):
        super(Theme, self).__init__()
        self.arg = arg
        