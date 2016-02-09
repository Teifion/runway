from ...base import DBSession
from ...system.models.user import User
from ..models import APIKey, APIHandler
from sqlalchemy import and_
from random import choice
import string

_handlers = {}

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

def collect_handlers():
    for h in APIHandler.__subclasses__():
        _handlers[h.name] = h

def get_key_by_user(user_id):
    return DBSession.query(
        APIKey
    ).filter(
        APIKey.user == user_id,
    ).first()

def test_response(result, msg=""):
    """
    Utility function for unit testing, checks for errors.
    """
    body = result.body.decode("utf-8")
    
    if body == "Key not found":
        return "No API key supplied{}".format(msg)
    
    if body[:17] == "Request mode of '" and body[-14:] == "' is not valid":
        return "Invalid mode{}".format(msg)
    
    return False
