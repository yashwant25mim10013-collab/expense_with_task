import customtkinter as ctk
from datetime import date
from components.cards import StatCard
from components.header import Header
from models.expense_model import ExpenseModel
from models.task_model import TaskModel
from models.budget_model import BudgetModel
from utils.date_utils import month_range
from utils.helpers import money

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure(2, weight=1)

        Header(self, "Dashboard").grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 15))

        self.today_card = StatCard(self, "Today's Expense", "₹0", "💰")
        self.month_card = StatCard(self, "Monthly Expense", "₹0", "📊")
        self.pending_card = StatCard(self, "Pending Tasks", "0", "📋")
        self.budget_card = StatCard(self, "Budget Remaining", "₹0", "💳")

        for i, card in enumerate([self.today_card, self.month_card, self.pending_card, self.budget_card]):
            card.grid(row=1, column=i, padx=6, sticky="nsew")

        self.recent = ctk.CTkTextbox(self, height=350)
        self.recent.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=(15,0))
        self.refresh()

    def refresh(self):
        start, end = month_range()
        today = date.today().isoformat()
        today_total = ExpenseModel.total_between(self.app.user_id,today,today)
        month_total = ExpenseModel.total_between(self.app.user_id,start,end)
        counts = TaskModel.counts(self.app.user_id)
        budget = BudgetModel.get(self.app.user_id, start[:7])
        remaining = (float(budget["amount"]) - month_total) if budget else 0

        self.today_card.set_value(money(today_total, self.app.currency))
        self.month_card.set_value(money(month_total, self.app.currency))
        self.pending_card.set_value(str(counts["Pending"] + counts["In Progress"]))
        self.budget_card.set_value(money(remaining, self.app.currency))

        self.recent.configure(state="normal")
        self.recent.delete("1.0", "end")
        self.recent.insert("end", "RECENT EXPENSES\n" + "─"*55 + "\n")
        for r in ExpenseModel.get_all(self.app.user_id)[:8]:
            self.recent.insert("end", f'{r["date"]}  |  {r["category"]:<15} | {money(r["amount"], self.app.currency)} | {r["description"] or ""}\n')
        self.recent.insert("end", "\nTODAY'S / UPCOMING TASKS\n" + "─"*55 + "\n")
        for r in TaskModel.get_all(self.app.user_id)[:8]:
            self.recent.insert("end", f'{r["due_date"]}  |  {r["priority"]:<6} | {r["status"]:<12} | {r["title"]}\n')
        self.recent.configure(state="disabled")
