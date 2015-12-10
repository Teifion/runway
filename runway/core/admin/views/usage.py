from pyramid.httpexceptions import HTTPFound

from ..lib import searches, admin_f, usage_f
from ...system.lib import user_f, auth
from ...lib import date_f, common
from ...system.models.user import User

from datetime import date, timedelta

def home(request):
    layout      = common.render("viewer")
    
    return dict(
        title       = "Admin: Home",
        layout      = layout,
    )

def user_search(request):
    layout      = common.render("viewer")
    
    page = int(request.params.get('page', 1))
    
    results = []
    if "username" in request.params:
        results = tuple(searches.by_username(request.params['username'], page=page))
    
    if len(results) == 1 and 'page' not in request.params:
        return HTTPFound(location=request.route_url('admin.usage.user.overview', user_id=results[0].id))
    
    return dict(
        title       = "Usage: User search",
        layout      = layout,
        results     = results,
        page        = page,
    )

def user_history(request):
    layout      = common.render("viewer")
    
    start_date, end_date = date_f.get_start_and_end_dates(request.params, period=timedelta(days=15))
    
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'page': int(request.params.get('page', 1)),
    }
    
    user_id = int(request.matchdict['user_id'])
    the_user = user_f.get_user(user_id)
    message = None
    
    user_logs = usage_f.user_history(user_id, start_date, date_f.end_of_day(end_date), page=params['page'])
    
    return dict(
        title       = "Usage: User overview",
        layout      = layout,
        user_logs   = user_logs,
        message     = message,
        the_user    = the_user,
        params      = params,
    )

def user_overview(request):
    layout      = common.render("viewer")
    
    start_date, end_date = date_f.get_start_and_end_dates(request.params, period=timedelta(days=15))
    
    params = {
        'start_date': start_date,
        'end_date': end_date,
    }
    
    user_id = int(request.matchdict['user_id'])
    the_user = user_f.get_user(user_id)
    message = None
    
    sections = usage_f.user_sections(user_id, start_date, date_f.end_of_day(end_date))
    
    return dict(
        title       = "Usage: User overview",
        layout      = layout,
        sections    = sections,
        message     = message,
        the_user    = the_user,
        params      = params,
    )


def group_search(request):
    layout      = common.render("viewer")
    
    results = []
    if "group" in request.params:
        group_name = request.params['group']
        
        if group_name in auth.group_lookup:
            return HTTPFound(location=request.route_url('admin.usage.group.overview', group_id=group_name))
            
        for g in auth.group_lookup.keys():
            if group_name.lower() in g.lower() or group_name == "*":
                results.append(g)
    
    if len(results) == 1:
        return HTTPFound(location=request.route_url('admin.usage.group.overview', group_id=results[0]))
    
    return dict(
        title       = "Usage: Group search",
        layout      = layout,
        results     = results,
    )

def group_history(request):
    layout      = common.render("viewer")
    
    start_date, end_date = date_f.get_start_and_end_dates(request.params, period=timedelta(days=15))
    
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'page': int(request.params.get('page', 1)),
    }
    
    group_id = request.matchdict['group_id']
    the_group = auth.ag_lookup[group_id]
    message = None
    
    user_logs = usage_f.group_history(group_id, start_date, date_f.end_of_day(end_date), page=params['page'])
    
    return dict(
        title       = "Usage: Group overview",
        layout      = layout,
        user_logs   = user_logs,
        message     = message,
        the_group   = the_group,
        group_id    = group_id,
        params      = params,
    )

def group_overview(request):
    layout      = common.render("viewer")
    
    start_date, end_date = date_f.get_start_and_end_dates(request.params, period=timedelta(days=15))
    
    params = {
        'start_date': start_date,
        'end_date': end_date,
    }
    
    group_id = request.matchdict['group_id']
    the_group = auth.ag_lookup[group_id]
    message = None
    
    sections = usage_f.group_sections(group_id, start_date, date_f.end_of_day(end_date))
    
    return dict(
        title       = "Usage: Group overview",
        layout      = layout,
        sections    = sections,
        message     = message,
        the_group   = the_group,
        group_id    = group_id,
        params      = params,
    )

def latest(request):
    layout      = common.render("viewer")
    
    mode = request.params.get("mode", "loggedin")
    
    user_logs = usage_f.latest_logs(mode)
    
    return dict(
        title       = "Usage: Latest logs",
        layout      = layout,
        user_logs   = user_logs,
        mode        = mode,
    )

def aggregate(request):
    layout      = common.render("viewer")
    
    start_date, end_date = date_f.get_start_and_end_dates({}, period="last 100 days")
    
    charts = usage_f.aggregate_charts(start_date, end_date)
    
    return dict(
        title       = "Usage: Latest logs",
        layout      = layout,
        
        total_views = charts['total_views']('total_views'),
        unique_views = charts['unique_views']('unique_views'),
        load_times = charts['load_times']('load_times'),
    )
