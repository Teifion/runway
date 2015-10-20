from sqlalchemy import func, and_
from ...base import DBSession
from ...system.models.user import User, UserPermissionGroup
from ...system.models import ViewLog, LogAggregate

def get_stats():
    return {
        "active_users": DBSession.query(func.count(User.id)).filter(User.id > 2, User.active == True).first()[0]
    }

