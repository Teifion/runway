from datetime import datetime, timedelta, date

biz_start = 9
biz_end = 18
biz_hours = biz_end - biz_start

def _biz_bound(the_date):
    # If it's after office hours, jump to next day
    if the_date.hour > biz_end:
        d = the_date + timedelta(days=1)
        return datetime(d.year, d.month, d.day, hour=biz_start)
    
    # If it's before office hours, jump to later that day
    if the_date.hour < biz_start:
        return datetime(the_date.year, the_date.month, the_date.day, hour=biz_start)
    
    return the_date

def _dmy(the_date):
    return (the_date.year, the_date.month, the_date.day)

def biz_days(start_date, end_date):
    """
    Returns a timedelta of the amount of actual business time between the two points.
    
    Calculate how many biz hours there are since the start of the day on the end date
    Calculate how many biz hours there are until the end of the day on the start date
    Calculate how many work-days there are between the two
    """
    if end_date < start_date:
        raise ValueError("start_date cannot be greater than end_date (start_date = {}, end_date = {})".format(str(start_date), str(end_date)))
    
    end_date = _biz_bound(end_date)
    start_date = _biz_bound(start_date)
    
    # Are they the same day?
    if _dmy(end_date) == _dmy(start_date):
        return end_date - start_date
    
    # Get the number of hours left of each day
    hours = (biz_end - start_date.hour) + (end_date.hour - biz_start)
    
    end_d = date(*_dmy(end_date))
    start_d = date(*_dmy(start_date))
    
    days = (end_d - start_d).total_seconds()/86400
    days = int(days-1)
    
    if days < 1:
        return timedelta(hours=hours)
    
    # At this point we need to see if we're dealing with any weekends
    list_of_days = (start_d + timedelta(days=d) for d in range(1, days+1))
    prelude      = lambda d: d.weekday() < 5
    weekdays     = len(list(filter(prelude, list_of_days)))
    
    return timedelta(hours=weekdays*biz_hours + hours)


def last_month(current_month = None):
    if current_month is None:
        y, m = datetime.today().year, datetime.today().month
    else:
        y, m = current_month.year, current_month.month
    
    m -= 1
    if m == 0:
        y -= 1
        m = 12
    
    return y, m

def get_start_of_month(today=None):
    if today is None:
        today = datetime.today()
    
    return datetime(
        year = today.year,
        month = today.month,
        day = 1,
    )

def get_start_of_year(today=None):
    if today is None:
        today = datetime.today()
    
    return datetime(
        year = today.year,
        month = 1,
        day = 1,
    )

def get_start_and_end_dates(params, period="month to date", start_date='start_date', end_date='end_date'):
    """
    Takes the request params and searches for the start and
    end dates. If it finds none it applies defaults, if it 
    finds data it converts it and applies some basic validation
    
    period can take a timedelta or "month to date"
    
    returns a (start_date, end_date) pair
    """
    
    period = period.lower()
    
    found_end = datetime.today() + timedelta(days=1)
    if params.get('end_date', '').strip() != '':
        found_end = datetime.strptime(params['end_date'], '%Y-%m-%d')
    
    if params.get('start_date', '').strip() != '':
        found_start = datetime.strptime(params['start_date'], '%Y-%m-%d')
    else:
        if isinstance(period, str):
            if period == "month to date":
                found_start = datetime(
                    year = found_end.year,
                    month = found_end.month,
                    day = 1,
                )
            
            elif period == 'last month':
                y, m = last_month(found_end)
                
                found_start = datetime(y, m, 1)
                
                # Found start is 00:00 on the 1st of the selected month
                found_end = datetime(
                    year = found_end.year,
                    month = found_end.month,
                    day = 1,
                )
            
            elif period == 'year to date':
                found_start = datetime(found_end.year, 1, 1)
            
            elif period == 'last year':
                found_start = datetime(found_end.year-1, 1, 1)
                found_end = datetime(found_end.year-1, 12, 31, 23, 59, 59)
            
            elif period == 'all time':
                found_start = datetime(1,1,1)
            
            elif period == 'last 100 days':
                found_start = found_end - timedelta(days=100)
            
            elif period == 'last 12 months':
                found_start = datetime(found_end.year-1, found_end.month, 1)
                
            else:
                raise ValueError("No handler for period type of '{}'".format(period))
            
        elif isinstance(period, timedelta):
            found_start = found_end - period
            
        else:
            raise ValueError("No handler for period valuetype of '{}'".format(type(period)))
    
    return found_start, found_end

date_presets = ("Month to date", "Last month", "Year to date", "Last year", "All time", "Custom dates")

def get_last_month():
    """
    Returns a datetime representing the start of the month
    before the current one and another datetime for the end
    of said month
    """
    
    now = datetime.now()
    
    return now, now

def end_of_day(the_datetime):
    """
    Takes a datetime and returns the same datetime but at the end of the day
    """
    return datetime(
        year   = the_datetime.year,
        month  = the_datetime.month,
        day    = the_datetime.day,
        hour   = 23,
        minute = 59,
        second = 59,
    )
