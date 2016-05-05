from ..models import (
    Channel,
    Subscription,
)
from ....core.system.models.user import User
from ....core.system.lib import user_f
from ....core.base import DBSession
import transaction
from sqlalchemy.orm import aliased
from sqlalchemy import and_

def get_channels(owner, *other_tables):
    fields     = [Channel]
    filters    = []
    joins      = []
    outerjoins = []
    
    if owner != None:
        filters.append(Channel.owner == owner)
    
    # By using a loop we take into account the order of the arguments
    for t in other_tables:
        if t == "owner":
            owner_table = aliased(User, name="owner_table")
            fields.append(owner_table)
            outerjoins.append((owner_table, and_(owner_table.id == Channel.owner)))
    
    return DBSession.query(*fields).filter(*filters).join(*joins).outerjoin(*outerjoins)

def get_channel(channel_id):
    return DBSession.query(
        Channel
    ).filter(
        Channel.id == channel_id
    ).first()

def add_channel(the_channel, return_id=False):
    DBSession.add(the_channel)
    
    if return_id:
        return DBSession.query(
            Channel.id,
        ).filter(
            Channel.sys_name == the_channel.sys_name,
        ).ordery_by(
            Channel.id.desc()
        ).first()[0]

def delete_channel(the_channel):
    DBSession.delete(the_channel)

def add_subscriptions(channel_id, *user_ids):
    DBSession.query(Subscription).filter(Subscription.channel == channel_id, Subscription.user.in_(user_ids)).delete(synchronize_session='fetch')
    
    inserts = []
    
    for u in user_ids:
        inserts.append({"user":u, "channel":channel_id})
    
    DBSession.bulk_insert_mappings(Subscription, inserts)

def get_subscriptions(channel_id, get_users=False):
    if not get_users:
        return DBSession.query(Subscription).filter(Subscription.channel == channel_id)
    else:
        return DBSession.query(
            Subscription,
            User
        ).join(
            (User, (User.id == Subscription.user)),
        ).filter(
            Subscription.channel == channel_id
        )
