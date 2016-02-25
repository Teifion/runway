from sqlalchemy import func, and_
from ...base import DBSession
from ...system.models.user import User, UserPermissionGroup
from ...system.models import ViewLog, LogAggregate

from ....core.nvd3 import pie_chart, line_chart, column_chart, colours
from datetime import datetime, timedelta

def user_sections(user_id, start_date, end_date):
    return DBSession.query(
        ViewLog.section,
        func.count(ViewLog.id),
    ).filter(
        ViewLog.user == user_id,
        ViewLog.timestamp > start_date,
        ViewLog.timestamp < end_date,
    ).group_by(
        ViewLog.section,
    ).order_by(
        func.count(ViewLog.id).desc(),
    )

def user_history(user_id, start_date, end_date, page=1, items_per_page=40):
    return DBSession.query(
        ViewLog
    ).filter(
        ViewLog.user == user_id,
        ViewLog.timestamp > start_date,
        ViewLog.timestamp < end_date,
    ).order_by(
        ViewLog.timestamp.desc(),
    ).offset(
        (page-1) * items_per_page
    ).limit(
        items_per_page
    )

def group_sections(group_id, start_date, end_date):
    return DBSession.query(
        ViewLog.section,
        func.count(ViewLog.id),
    ).filter(
        ViewLog.user == UserPermissionGroup.user,
        ViewLog.timestamp > start_date,
        ViewLog.timestamp < end_date,
    ).outerjoin(
        (UserPermissionGroup, and_(
            UserPermissionGroup.group == group_id,
        )),
    ).group_by(
        ViewLog.section,
    ).order_by(
        func.count(ViewLog.id).desc(),
    )

def group_history(group_id, start_date, end_date, page=1, items_per_page=40):
    return DBSession.query(
        ViewLog,
        User.username,
    ).filter(
        ViewLog.user == UserPermissionGroup.user,
        ViewLog.timestamp > start_date,
        ViewLog.timestamp < end_date,
        User.id == ViewLog.user,
    ).outerjoin(
        (UserPermissionGroup, and_(
            UserPermissionGroup.group == group_id,
        )),
    ).order_by(
        ViewLog.timestamp.desc(),
    ).offset(
        (page-1) * items_per_page
    ).limit(
        items_per_page
    )

def latest_logs(mode="all", items_per_page=40):
    if mode == "loggedin":
        filters = [User.id != 2, User.id != 1]
    else:
        filters = [User.id != 1]
    
    # Now the actual query
    return DBSession.query(
        ViewLog,
        User.username,
    ).filter(
        *filters
    ).outerjoin(
        (User, and_(
            User.id == ViewLog.user,
        )),
    ).order_by(
        ViewLog.timestamp.desc(),
    ).limit(
        items_per_page
    )

def aggregate_charts(start_date, end_date, *filters):
    query = DBSession.query(
        LogAggregate,
    ).filter(
        LogAggregate.date >= start_date,
        LogAggregate.date <= end_date,
        LogAggregate.section == "*"
    ).order_by(
        LogAggregate.date.asc()
    )
    
    total_views = []
    unique_views = []
    load_times = []
    for row in query:
        total_views.append(
            [row.date.strftime("%d/%m/%Y"), float(row.page_views[24])]
        )
        unique_views.append(
            [row.date.strftime("%d/%m/%Y"), float(row.unique_users[24])]
        )
        load_times.append(
            [row.date.strftime("%d/%m/%Y"), float(row.load_times[24])]
        )
    
    total_lines = [{
        "values": total_views,
        "key": 'Total views',
        "color": '#0000AA'
    }]
    unique_lines = [{
        "values": unique_views,
        "key": 'Unique views',
        "color": '#AA00AA'
    }]
    load_lines = [{
        "values": load_times,
        "key": 'Load times',
        "color": '#AA0000'
    }]
    
    return {
        "total_views": line_chart(start_date, end_date, total_lines, y_label="Views"),
        "unique_views": line_chart(start_date, end_date, unique_lines, y_label="Views"),
        "load_times": line_chart(start_date, end_date, load_lines, y_label="Average Load time (seconds)", tick_format=",.3f"),
    }

def daily_tally(the_date=None):
    if the_date is None:
        the_date = datetime.today()
    
    the_date = datetime(the_date.year, the_date.month, the_date.day)
    
    return DBSession.query(
        func.count(ViewLog.id),
    ).filter(
        ViewLog.timestamp >= the_date,
        ViewLog.timestamp < (the_date + timedelta(days=1)),
    ).first()[0]
