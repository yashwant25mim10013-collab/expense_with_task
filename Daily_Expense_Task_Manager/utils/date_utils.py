from datetime import date, datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"

def today_str():
    return date.today().strftime(DATE_FORMAT)

def parse_date(value):
    return datetime.strptime(value, DATE_FORMAT).date()

def month_range(year=None, month=None):
    d = date.today()
    year = year or d.year
    month = month or d.month
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(year, month + 1, 1) - timedelta(days=1)
    return start.strftime(DATE_FORMAT), end.strftime(DATE_FORMAT)

def is_overdue(due_date):
    try:
        return parse_date(due_date) < date.today()
    except Exception:
        return False
