from ...core.lib.base import DBSession
from ...core.models.user import User

def by_username(terms):
    return DBSession.query(User).filter(User.username.like('%{}%'.format(terms)))
