import re
import datetime
import time
import transaction
from sqlalchemy import func, or_

from ...base import DBSession

# from ..models import (
#     UserLog,
#     LogStats,
#     ActionLog,
# )

ignored_filetypes = re.compile(r"(css|js|html|png|jpg|jpeg|ico|gif)$")
section_grep = re.compile(r"(?:/venustate)?/([a-zA-Z0-9_]+?)/")

# def log_action(admin_user_id, action_type, **kwargs):
#     l = ActionLog()
    
#     l.when        = datetime.datetime.now()
#     l.user        = admin_user_id
#     l.action_type = action_type
#     l.kwargs      = json.dumps(kwargs)
    
#     with transaction.manager:
#         stmt = """INSERT INTO action_logs
#         ("when", "agent", "action_type", "kwargs") VALUES
#         (:when, :agent, :action_type, :kwargs);"""
        
#         args = dict(
#             when        = l.when,
#             agent       = l.user,
#             action_type = l.action_type,
#             kwargs      = l.kwargs,
#         )
        
#         # For some reason it won't let us use DBSession.add()
#         DBSession.execute(stmt, args)
#         DBSession.execute("COMMIT")

# def _get_logs(start, end_date, interval, **kwargs):
#     """Main function for getting data"""
#     wheres = []
#     join_to_users = False
    
#     # Query period
#     wheres.append(UserLog.timestamp >= start-interval)
#     wheres.append(UserLog.timestamp <= end_date+interval)
    
#     if "include_refreshes" not in kwargs:
#         wheres.append(UserLog.refresh == False)
    
#     # Where filters
#     if "doc" in kwargs:
#         if type(kwargs["doc"]) == int:
#             wheres.append(UserLog.doc == kwargs["doc"])
#         else:
#             wheres.append(UserLog.doc.in_(kwargs["doc"]))
    
#     if "poll" in kwargs:
#         if type(kwargs["poll"]) == int:
#             wheres.append(UserLog.poll == kwargs["poll"])
#         else:
#             wheres.append(UserLog.poll.in_(kwargs["poll"]))
    
#     if "path" in kwargs:
#         if kwargs['path'] not in ("", "*"):
#             kwargs['path'] = kwargs['path'].replace("%", "\\%")
#             wheres.append(UserLog.path.like("%{}%".format(kwargs['path'])))
    
#     if "location" in kwargs:
#         if kwargs['location'] != common.locations.index("All"):
#             join_to_users = True
#             wheres.append(User.location == kwargs['location'])
    
#     if "department" in kwargs:
#         if kwargs['department'] != common.departments.index("All"):
#             join_to_users = True
#             wheres.append(User.department == kwargs['department'])
    
#     if "user_id" in kwargs:
#         if kwargs['user_id'] != 0:
#             wheres.append(UserLog.user == int(kwargs['user_id']))
    
#     if join_to_users:
#         wheres.append(UserLog.user == User.id)
    
#     # Custom wheres
#     if "where" in kwargs:
#         wheres.append(kwargs['where'])
    
#     # Do we just want the wheres?
#     if kwargs.get('just_wheres', False):
#         data = OrderedDict()
#         data.wheres = wheres
#         return data
    
#     # Pull data from the database
#     results = DBSession.query(UserLog.timestamp, UserLog.load_time).filter(*wheres).order_by(UserLog.timestamp)
    
#     if interval == datetime.timedelta(hours=1):
#         grouper = lambda row: (row[0].year, row[0].month, row[0].day, row[0].hour)
    
#     elif interval == datetime.timedelta(days=1):
#         grouper = lambda row: (row[0].year, row[0].month, row[0].day)
    
#     elif interval == datetime.timedelta(days=7):
#         grouper = lambda row: (row[0].year, row[0].month, math.floor(row[0].day/7))
    
#     elif interval == datetime.timedelta(days=30):
#         grouper = lambda row: (row[0].year, row[0].month, math.floor(row[0].day/30))
    
#     # Make empty points
#     points = OrderedDict()
#     c_date = start
    
#     while c_date <= end_date:
#         points[grouper([c_date])] = []
#         c_date += interval
    
#     for (time_group, rows) in groupby(results, grouper):
#         points[time_group] = []
#         for row in rows:
#             points[time_group].append(row[1])
    
#     data = Dataset(OrderedDict())
#     data.start    = start
#     data.end_date   = end_date
#     data.interval = interval
    
#     data.wheres = wheres
#     data.selects = (UserLog.timestamp,)
#     data.query = results.statement
    
#     ld, ld2 = None, None
#     for d, v in points.items():
#         if len(v) > 0:
#             data[d] = len(v)
#         else:
#             data[d] = 0
        
#         ld2 = ld
#         ld = d
    
#     # For some reason the last two need to be swapped back around
#     try:
#         data[ld], data[ld2] = data[ld2], data[ld]
#     except Exception:
#         pass
    
#     return data

# def _game_path_test(path):
#     return any((
#         ("wordy" in path),
#         ("connect_four" in path),
#         ("ultimate_ox" in path),
#         ("odummo" in path),
#     ))

# def _blank_logstats(the_date, location, department):
#     end_date = the_date + datetime.timedelta(days=1)
    
#     filters = [
#         User.id == UserLog.user,
#         UserLog.timestamp >= the_date,
#         UserLog.timestamp < end_date,
#     ]
    
#     # If it's all, get all the stats!
#     if common.locations[location] != "All":
#         filters.append(User.location == location)
    
#     if common.departments[department] != "All":
#         filters.append(User.department == department)
    
#     # Build the empty log stats object
#     the_stats            = LogStats()
#     the_stats.date       = the_date
#     the_stats.location   = location
#     the_stats.department = department
#     the_stats.prep()
    
#     def _add_to_list(the_list, user_id, load_time):
#         the_list[0] += 1
#         the_list[1].add(user_id)
#         the_list[2].append(load_time)
    
#     for log, uid in DBSession.query(UserLog, User.id).filter(*filters):
#         # Views, Uniques, Average load time
#         _add_to_list(the_stats.total, uid, log.load_time)
        
#         # if log.path[0:16] == "/venustate/games":
#         if _game_path_test(log.path):
#             _add_to_list(the_stats.path_games, uid, log.load_time)
#             the_stats.users_games.add(uid)
        
#         if "/FandT" in log.path:
#             _add_to_list(the_stats.path_fandt, uid, log.load_time)
#             the_stats.users_fandt.add(uid)
        
#         if "/training" in log.path:
#             _add_to_list(the_stats.path_training, uid, log.load_time)
#             the_stats.users_training.add(uid)
        
#         if "/compare" in log.path:
#             _add_to_list(the_stats.path_compare, uid, log.load_time)
#             the_stats.users_compare.add(uid)
        
#         if "/pipeline" in log.path:
#             _add_to_list(the_stats.path_pipeline, uid, log.load_time)
#             the_stats.users_pipeline.add(uid)
        
#         if log.announcement != None:
#             _add_to_list(the_stats.path_announcements, uid, log.load_time)
#             the_stats.users_announcements.add(uid)
        
#         if log.path[0:14] == "/venustate/sms":
#             _add_to_list(the_stats.path_sms, uid, log.load_time)
#             the_stats.users_sms.add(uid)
        
#         if log.path[0:23] == "/venustate/achievements":
#             _add_to_list(the_stats.path_achievements, uid, log.load_time)
#             the_stats.users_achievements.add(uid)
        
#         # 0-1, 1-2, 2-3 ... 22-23, 23-24
#         log_hour = log.timestamp.hour
#         the_stats.hourly_views[log_hour] += 1
#         the_stats.hourly_uniques[log_hour].add(uid)
#         the_stats.hourly_load_time[log_hour].append(log.load_time)
        
#         the_stats.userlist.add(uid)
    
#     the_stats.flatten()
#     return the_stats

# def build_day_stats(year, month, day):
#     """
#     Calculate the stat aggregates for the day
#     """
#     the_date = datetime.datetime(year=year, month=month, day=day)
#     delete_log_date = the_date-datetime.timedelta(days=65)
    
#     with transaction.manager:
#         DBSession.query(UserLog).filter(UserLog.timestamp < delete_log_date).delete()
#         DBSession.query(LogStats).filter(LogStats.date == the_date).delete()
    
#     for l in range(len(common.locations)):
#         # Only 4 main departments and ALL
#         for d in (1,2,3,4,5):
#             the_stats = _blank_logstats(the_date, l, d)
            
#             with transaction.manager:
#                 DBSession.add(the_stats)
