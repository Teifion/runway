from ..models import (
    NewsItem,
)
from ....core.system.models.user import User
from ....core.system.lib import user_f
from ....core.base import DBSession
import transaction
from sqlalchemy.orm import aliased
from sqlalchemy import and_

def get_items(channel, *other_tables):
    fields     = [NewsItem]
    filters    = []
    joins      = []
    outerjoins = []
    
    if channel != None:
        filters.append(NewsItem.channel == channel)
    
    # By using a loop we take into account the order of the arguments
    for t in other_tables:
        if t == "poster":
            poster_table = aliased(User, name="poster_table")
            fields.append(poster_table)
            outerjoins.append((poster_table, and_(poster_table.id == NewsItem.poster)))
    
    return DBSession.query(*fields).filter(*filters).join(*joins).outerjoin(*outerjoins)

def get_item(item_id, *other_tables):
    fields     = [NewsItem]
    filters    = [NewsItem.id == item_id]
    joins      = []
    outerjoins = []
    
    # By using a loop we take into account the order of the arguments
    for t in other_tables:
        if t == "poster":
            poster_table = aliased(User, name="poster_table")
            fields.append(poster_table)
            joins.append((poster_table, and_(poster_table.id == NewsItem.poster)))
        
        if t == "channel":
            channel_table = aliased(Folder, name="channel_table")
            fields.append(channel_table)
            outerjoins.append((channel_table, and_(channel_table.id == NewsItem.channel)))
    
    return DBSession.query(*fields).filter(*filters).join(*joins).outerjoin(*outerjoins).first()


def add_item(the_item, return_id=False):
    DBSession.add(the_item)
    
    if return_id:
        return DBSession.query(
            NewsItem.id,
        ).filter(
            NewsItem.sys_name == the_item.sys_name,
        ).ordery_by(
            NewsItem.id.desc()
        ).first()[0]

def delete_item(the_item):
    DBSession.delete(the_item)
