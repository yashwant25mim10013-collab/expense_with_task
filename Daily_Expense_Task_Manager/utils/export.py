
from pathlib import Path
import csv
from models.expense_model import ExpenseModel
from models.task_model import TaskModel

EXPORT_DIR=Path(__file__).resolve().parents[1]/"exports"
for x in ("expenses","tasks","reports"): (EXPORT_DIR/x).mkdir(parents=True,exist_ok=True)

def export_expenses_csv(user_id,path=None):
    path=Path(path or EXPORT_DIR/"expenses"/"expenses.csv")
    rows=ExpenseModel.get_all(user_id)
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["ID","Date","Amount","Category","Description","Payment Method"])
        for r in rows: w.writerow([r["id"],r["date"],r["amount"],r["category"],r["description"],r["payment_method"]])
    return path

def export_tasks_csv(user_id,path=None):
    path=Path(path or EXPORT_DIR/"tasks"/"tasks.csv")
    rows=TaskModel.get_all(user_id)
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["ID","Title","Description","Due Date","Priority","Category","Status"])
        for r in rows: w.writerow([r["id"],r["title"],r["description"],r["due_date"],r["priority"],r["category"],r["status"]])
    return path
