
from datetime import date, timedelta
from models.expense_model import ExpenseModel
from models.task_model import TaskModel
from models.budget_model import BudgetModel
from utils.date_utils import month_range

def generate_insights(user_id):
    start,end=month_range()
    cats=ExpenseModel.category_totals(user_id,start,end)
    total=ExpenseModel.total_between(user_id,start,end)
    counts=TaskModel.counts(user_id)
    budget=BudgetModel.get()
    insights=[]
    if total == 0:
        insights.append("No expenses recorded this month yet. Add transactions to receive spending insights.")
    else:
        if cats:
            top=cats[0]
            share=(top["total"]/total)*100
            insights.append(f"{top['category']} is your largest spending category at {share:.1f}% of monthly spending.")
        if budget and total > float(budget["amount"]):
            insights.append("Your current monthly spending is above the configured budget.")
        elif budget:
            remaining=float(budget["amount"])-total
            insights.append(f"You have approximately ₹{remaining:,.2f} remaining in the configured monthly budget.")
    total_tasks=sum(counts.values())
    if total_tasks:
        rate=counts["Completed"]/total_tasks*100
        insights.append(f"Task completion rate is {rate:.1f}% ({counts['Completed']} of {total_tasks} tasks).")
        if counts["Pending"]>5:
            insights.append("You have more than five pending tasks; consider reviewing priorities and due dates.")
    else:
        insights.append("No tasks are recorded yet. Add tasks to track your workload.")
    return insights
