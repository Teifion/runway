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

from ...core.base import Base

class APIKey(Base):
    __tablename__ = 'runway_api_keys'
    id            = Column(Integer, primary_key=True)
    user          = Column(Integer, ForeignKey("runway_users.id"), nullable=True)
    key           = Column(String, nullable=False)


class APIHandler(object):
    """
    You are required to define the following fields
    
    name -> Machine name of the handler, I'd suggest the use of a namespace
    group -> Human readable name of the grouping for the handler
    label -> Human readable name of the handler
    description -> Human readable description of the handler, designed to inform
        end users about what the handler does and when/where it will fire
    documentation -> HTML content explaining how the trigger works, like a description
        but in a lot more detail, it is shown to the users when they click an "info" button
    location -> The location of the file itself
    
    Optionally:
    permissions -> A list of permissions required to use this handler
    """
    
    permissions = []
    
    def __call__(self, request, test_mode=False):
        """
        Called as part of the action system, it should return a
        string (typically JSON) which will be returned as the
        result of the API itself.
        
        It needs to accept the request object and a boolean flag of "test_mode"
        which will allow testing at a reduced functionality by the live system
        for displaying results or testing basic functionality. Your unit tests
        do not need to call it in test mode.
        """
        raise Exception("Not implemented by {} handler".format(self.name))
