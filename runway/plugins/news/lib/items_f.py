from ..models import (
    Item,
    ItemLog,
)
from ....core.system.models.user import User
from ....core.system.lib import user_f
from ....core.base import DBSession
import transaction
from sqlalchemy.orm import aliased
from sqlalchemy import and_
from datetime import datetime

# Most of these are not in use but have been put in incase I want to use them at a later date
log_states = (
    "N/A",
    "unread",
    "read",
    "signed",
)

def get_items(channel, *other_tables):
    fields     = [Item]
    filters    = []
    joins      = []
    outerjoins = []
    
    if channel != None:
        filters.append(Item.channel == channel)
    
    # By using a loop we take into account the order of the arguments
    for t in other_tables:
        if t == "poster":
            poster_table = aliased(User, name="poster_table")
            fields.append(poster_table)
            outerjoins.append((poster_table, and_(poster_table.id == Item.poster)))
    
    return DBSession.query(*fields).filter(*filters).join(*joins).outerjoin(*outerjoins)

def get_item(item_id, *other_tables):
    fields     = [Item]
    filters    = [Item.id == item_id]
    joins      = []
    outerjoins = []
    
    # By using a loop we take into account the order of the arguments
    for t in other_tables:
        if t == "poster":
            poster_table = aliased(User, name="poster_table")
            fields.append(poster_table)
            joins.append((poster_table, and_(poster_table.id == Item.poster)))
        
        if t == "channel":
            channel_table = aliased(Folder, name="channel_table")
            fields.append(channel_table)
            outerjoins.append((channel_table, and_(channel_table.id == Item.channel)))
    
    return DBSession.query(*fields).filter(*filters).join(*joins).outerjoin(*outerjoins).first()


def add_item(the_item, return_id=False):
    DBSession.add(the_item)
    
    if return_id:
        return DBSession.query(
            Item.id,
        ).filter(
            Item.sys_name == the_item.sys_name,
        ).ordery_by(
            Item.id.desc()
        ).first()[0]

def delete_item(the_item):
    DBSession.delete(the_item)

def get_log(item_id, user_id):
    result = DBSession.query(ItemLog).filter(ItemLog.user == user_id, ItemLog.item == item_id).first()
    
    return result

_log_view_state = log_states.index("read")
def log_view(item_id, user_id, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()
    
    DBSession.add(ItemLog(
        user          = user_id,
        item          = item_id,
        state         = _log_view_state,
        timestamp     = timestamp,
    ))

_log_view_state = log_states.index("signed")
def log_signing(item_id, user_id, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()
    
    DBSession.add(ItemLog(
        user          = user_id,
        item          = item_id,
        state         = _log_signing_state,
        timestamp     = timestamp,
    ))
