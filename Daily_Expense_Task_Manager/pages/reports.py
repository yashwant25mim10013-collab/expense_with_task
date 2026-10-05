
import customtkinter as ctk
from components.header import Header
from components.dialogs import info,error
from utils.export import export_expenses_csv,export_tasks_csv
from utils.advanced_reports import create_pdf_report,backup_database
from models.expense_model import ExpenseModel
from models.task_model import TaskModel
from models.budget_model import BudgetModel
from utils.date_utils import month_range

class ReportsPage(ctk.CTkFrame):
    def __init__(self,master,app):
        super().__init__(master,fg_color="transparent"); self.app=app
        Header(self,"Reports, PDF & Backup").pack(anchor="w",pady=(0,15))
        buttons=[("Export Expenses CSV",self.expenses),("Export Tasks CSV",self.tasks),("Export Expenses Excel",self.excel),
                 ("Generate Advanced PDF Report",self.pdf),("Backup Database",self.backup)]
        for t,cmd in buttons: ctk.CTkButton(self,text=t,command=cmd,width=300).pack(anchor="w",pady=5)
        self.summary=ctk.CTkTextbox(self,height=270); self.summary.pack(fill="both",expand=True,pady=15)
        self.refresh()
    def refresh(self):
        start,end=month_range(); expenses=ExpenseModel.get_all(self.app.user_id); tasks=TaskModel.get_all(self.app.user_id)
        total=sum(float(r["amount"]) for r in expenses if start<=r["date"]<=end); b=BudgetModel.get()
        budget=float(b["amount"]) if b else 0
        self.summary.delete("1.0","end")
        self.summary.insert("end",f"CURRENT MONTH\n{'='*45}\nExpense: ₹{total:,.2f}\nBudget: ₹{budget:,.2f}\nRemaining: ₹{budget-total:,.2f}\nTasks: {len(tasks)}\nCompleted: {sum(1 for t in tasks if t['status']=='Completed')}\n")
    def expenses(self): info("Exported",str(export_expenses_csv(self.app.user_id)))
    def tasks(self): info("Exported",str(export_tasks_csv(self.app.user_id)))
    def excel(self):
        try:
            import pandas as pd
            path=__import__("pathlib").Path(__file__).resolve().parents[1]/"exports"/"expenses"/"expenses.xlsx"
            pd.DataFrame([dict(r) for r in ExpenseModel.get_all(self.app.user_id)]).to_excel(path,index=False)
            info("Exported",str(path))
        except Exception as e: error("Export failed",str(e))
    def pdf(self):
        try: info("PDF Created",str(create_pdf_report(self.app.user_id,self.app.display_name)))
        except Exception as e: error("PDF failed",str(e))
    def backup(self):
        try: info("Backup Created",str(backup_database()))
        except Exception as e: error("Backup failed",str(e))
