def valid_amount(value):
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False

def required(value):
    return bool(str(value).strip())

def valid_date(value):
    from datetime import datetime
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False
