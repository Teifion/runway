from sqlalchemy import func, or_, and_
from sqlalchemy.sql.expression import label
from ...base import DBSession
from ...system.models import ViewLog
import transaction

def get_slow_pages(path = None):
    l = label("average", func.avg(ViewLog.load_time))
    c = label("count", func.count(ViewLog.id))
    
    return DBSession.query(
        ViewLog.path,
        l,
        c,
        label("stddev", func.stddev_pop(ViewLog.load_time)),
        label("maximum", func.max(ViewLog.load_time)),
        label("minimum", func.min(ViewLog.load_time)),
    ).filter(
        ViewLog.path == path if path != None else True
    ).having(
        c > 2,
    ).group_by(
        ViewLog.path
    ).order_by(
        l.desc()
    )

def get_logs(path):
    return DBSession.query(ViewLog).filter(ViewLog.path == path).order_by(ViewLog.id.asc())

def get_neighbouring_logs(log_id, user=None, path=None, margin=10):
    # If we have no other filters, we can do it as one query really easily
    if user is None and path is None:
        return DBSession.query(
            ViewLog,
        ).filter(
            ViewLog.id >= log_id - margin,
            ViewLog.id <= log_id + margin,
        ).order_by(
            ViewLog.id.asc()
        )
    
    prior = list(DBSession.query(
        ViewLog,
    ).filter(
        ViewLog.id < log_id,
        ViewLog.user == int(user) if user != None else True,
        ViewLog.path == path if path != None else True,
    ).order_by(
        ViewLog.id.desc()
    ).limit(
        margin
    ))
    prior.reverse()
    
    after = list(DBSession.query(
        ViewLog,
    ).filter(
        ViewLog.id >= log_id,
        ViewLog.user == int(user) if user != None else True,
        ViewLog.path == path if path != None else True,
    ).order_by(
        ViewLog.id.asc()
    ).limit(
        (margin + 1)
    ))
    
    return prior + after
