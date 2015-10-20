from sqlalchemy import func, or_, and_
from ...base import DBSession
from ...system.models import ExceptionLog
from ...system.models.user import User
import transaction

def exception_count(user_id=None):
    query = DBSession.query(
        ExceptionLog.assigned,
        func.count(ExceptionLog.id)
    ).filter(
        or_(ExceptionLog.assigned == None, ExceptionLog.assigned == user_id),
        ExceptionLog.hidden == False,
    ).group_by(
        ExceptionLog.assigned
    )
    
    return {assigned:count for assigned, count in query}

def exception_list(user_id=None, show_all=False):
    query = DBSession.query(
        ExceptionLog,
        User,
    ).outerjoin(
        (User, and_(User.id == ExceptionLog.user)),
    ).filter(
        ExceptionLog.assigned == user_id,
        True if show_all else ExceptionLog.hidden == False,
    ).order_by(
        ExceptionLog.timestamp.desc()
    ).limit(40)
    
    return query

def get_exception(exception_id):
    return DBSession.query(ExceptionLog).filter(ExceptionLog.id == exception_id).first()

def hide_exception(exception_id):
    with transaction.manager:
        DBSession.execute("UPDATE {} SET hidden = True WHERE id = {:d}".format(ExceptionLog.__tablename__, exception_id))
        DBSession.execute("COMMIT")

def hide_all_exceptions():
    with transaction.manager:
        DBSession.execute("UPDATE {} SET hidden = True".format(ExceptionLog.__tablename__))
        DBSession.execute("COMMIT")
