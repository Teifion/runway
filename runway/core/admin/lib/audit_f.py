from sqlalchemy import and_, or_
from ...base import DBSession
from ...system.models import AuditLog
from ...system.models.user import (
    User,
)

def get_recent_logs():
    return DBSession.query(
        AuditLog,
        User,
    ).join(
        (User, and_(AuditLog.user == User.id)),
    ).order_by(
        AuditLog.timestamp.desc(),
    ).limit(
        25
    )
