from ..models import (
    NewsChannel,
)
from ....core.system.models.user import User
from ....core.system.lib import user_f
from ....core.base import DBSession
import transaction
from sqlalchemy.orm import aliased

def get_channels(owner, *other_tables):
    fields     = [NewsChannel]
    filters    = []
    joins      = []
    outerjoins = []
    
    if owner != None:
        filters.append(NewsChannel.owner == owner)
    
    # By using a loop we take into account the order of the arguments
    for t in other_tables:
        if t == "owner":
            owner_table = aliased(User, name="owner_table")
            fields.append(owner_table)
            outerjoins.append((owner_table, and_(owner_table.id == NewsChannel.owner)))
    
    return DBSession.query(*fields).filter(*filters).join(*joins).outerjoin(*outerjoins).first()
