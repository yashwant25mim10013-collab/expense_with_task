
from datetime import date,timedelta
from models.expense_model import ExpenseModel
from utils.date_utils import month_range
def summary(user_id):
    today=date.today(); today_s=today.isoformat(); week_start=today-timedelta(days=today.weekday())
    start,end=month_range()
    return {"today":ExpenseModel.total_between(user_id,today_s,today_s),
            "week":ExpenseModel.total_between(user_id,week_start.isoformat(),today_s),
            "month":ExpenseModel.total_between(user_id,start,end),
            "categories":ExpenseModel.category_totals(user_id,start,end),
            "daily":ExpenseModel.daily_totals(user_id,start,end)}
