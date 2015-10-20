from ...base import DBSession
from ...system.models.user import User
from ..models.models import APIKey
from sqlalchemy import and_
from random import choice
import string

def auth(key):
    the_key = DBSession.query(APIKey).filter(APIKey.key == key).first()
    return the_key

_chars = string.ascii_letters + string.digits
def grant(user_id):
    key_str = "".join(map(lambda i: choice(_chars), range(24)))
    
    the_key = APIKey(
        user = user_id,
        key = key_str,
    )
    
    DBSession.add(the_key)
    return the_key.key

def revoke(key_id):
    DBSession.query(APIKey).filter(APIKey.id == key_id).delete()

def get_key_list():
    return DBSession.query(
        User, APIKey
    ).join(
        (APIKey, and_(APIKey.user == User.id)),
    ).order_by(User.username)

def get_user_by_key(key_id):
    return DBSession.query(
        User
    ).join(
        (APIKey, and_(APIKey.user == User.id)),
    ).filter(
        APIKey.key == key_id,
    ).first()

handlers = {}
def register_handler(name, handler, permission):
    if name in handlers and handler != handlers[name][0]:
        raise KeyError("The handler by the name of {} already exists".format(name))
    
    handlers[name] = handler, permission
