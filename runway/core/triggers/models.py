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
from collections import namedtuple

class TriggerScript(Base):
    """
    This is the object stored in the database tracking what a user
    wants to happen. It is started by a Trigger and built from Actions.
    """
    
    __tablename__ = 'runway_trigger_scripts'
    id            = Column(Integer, primary_key=True)
    
    owner         = Column(Integer, ForeignKey("runway_users.id"), nullable=False, index=True)
    label         = Column(String, nullable=False)
    
    # The trigger this fires off to start with
    trigger       = Column(String, nullable=False, index=True)
    
    actions       = Column(Text, nullable=False, default="[]")
    comments      = Column(Text, nullable=False, default="")
    
    active        = Column(Boolean, nullable=False)
    valid_code    = Column(Boolean, nullable=False)


class Trigger(object):
    """
    You are required to define the following fields
    
    name -> Machine name of the trigger, I'd suggest the use of a namespace
    group -> Human readable name of the grouping for the trigger
    label -> Human readable name of the trigger
    description -> Human readable description of the trigger, designed to inform
        end users about what the trigger does and when/where it will fire
    documentation -> HTML content explaining how the trigger works, like a description
        but in a lot more detail, it is shown to the users when they click an "info" button
    outputs -> A sequence of 3 length tuples (name, type, description)
    examples -> A list of example outputs that could be produced by the trigger
    
    Optionally:
    permissions -> A list of permissions required to use this trigger
    example_inputs -> A list of dictionaries showing some possible inputs to the trigger
        the first example is used in the dev section to provide data for running the trigger
    """
    
    permissions = []
    example_inputs = []
    
    def __call__(self):
        """
        Called by the triggering function, it should return a
        dictionary conforming to the definition laid out in outputs
        """
        raise Exception("Not implemented by {} trigger".format(self.name))

class Action(object):
    """
    You are required to define the following fields
    
    name -> Machine name of the action, I'd suggest the use of a namespace
    group -> Human readable name of the grouping for the action
    label -> Human readable name of the action
    description -> Human readable description of the action, designed to inform
        end users about what the action does and when/where it will fire
    documentation -> HTML content explaining how the trigger works, like a description
        but in a lot more detail, it is shown to the users when they click an "info" button
    inputs -> A sequence of 3 length tuples (name, type, description)
        Note: An input named "args" of type list will be treated as a varadic input (*args)
        and the same will apply to "kwargs" of type dict (**kwargs)
    outputs -> A sequence of 3 length tuples (name, type, description), an empty sequence
        indicates no returned values (e.g. an email action)
    examples -> A list of example input to output combinations that could be produced
        by the action, the first example is used in the dev section to provide blank data
        
    Optionally:
    permissions -> A list of permissions required to use this action
    """
    
    permissions = []
    
    def __call__(self, test_mode=False):
        """
        Called as part of the action system, it should return a
        dictionary conforming to the definition laid out in outputs (or a None)
        
        Should always be able to accept a "test_mode" value to disable certain
        functionality (such as the sending of emails) to test reduced portions
        and thus to be tested in a generic and unguarded fashion.
        """
        raise Exception("Not implemented by {} action".format(self.name))
