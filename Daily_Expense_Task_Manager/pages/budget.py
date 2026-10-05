import customtkinter as ctk
from datetime import date, datetime

from components.header import Header
from components.dialogs import info, error
from models.budget_model import BudgetModel
from models.expense_model import ExpenseModel
from utils.date_utils import month_range
from utils.validators import valid_amount
from utils.helpers import money


class BudgetPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        Header(self, "Monthly Budget").pack(anchor="w", pady=(0, 15))

        box = ctk.CTkFrame(self)
        box.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            box,
            text="Set Monthly Budget",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 8))

        ctk.CTkLabel(
            box,
            text="Choose a month and enter the budget you want to spend that month."
        ).pack(pady=(0, 15))

        self.months = self._make_month_list()
        self.month_var = ctk.StringVar(value=self.months[0])
        self.month_menu = ctk.CTkOptionMenu(
            box,
            variable=self.month_var,
            values=self.months,
            command=lambda _: self.refresh()
        )
        self.month_menu.pack(padx=30, pady=8)

        self.amount = ctk.CTkEntry(
            box,
            placeholder_text="Enter monthly budget (e.g. 15000)",
            width=280
        )
        self.amount.pack(padx=30, pady=8)

        ctk.CTkButton(
            box,
            text="Save Monthly Budget",
            command=self.save,
            width=220
        ).pack(pady=10)

        self.info = ctk.CTkLabel(box, text="", justify="center")
        self.info.pack(pady=(10, 25))

        self.refresh()

    def _make_month_list(self):
        today = date.today()
        months = []
        for offset in range(-6, 7):
            month_index = today.month - 1 + offset
            year = today.year + month_index // 12
            month = month_index % 12 + 1
            value = f"{year:04d}-{month:02d}"
            label = datetime(year, month, 1).strftime("%B %Y")
            months.append(f"{label} ({value})")
        return months

    def _selected_month(self):
        return self.month_var.get().split("(")[-1].rstrip(")")

    def refresh(self):
        month = self._selected_month()
        budget = BudgetModel.get(self.app.user_id, month)

        year, month_num = map(int, month.split("-"))
        start = f"{month}-01"
        import calendar
        end = f"{month}-{calendar.monthrange(year, month_num)[1]:02d}"

        spent = ExpenseModel.total_between(self.app.user_id, start, end)
        amount = float(budget["amount"]) if budget else 0
        remaining = amount - spent

        self.amount.delete(0, "end")
        if budget:
            self.amount.insert(0, f"{amount:.2f}")

        status = "No budget set for this month." if not budget else "Budget is set for this month."

        self.info.configure(
            text=(
                f"{status}\n\n"
                f"Budget: {money(amount, self.app.currency)}\n"
                f"Spent: {money(spent, self.app.currency)}\n"
                f"Remaining: {money(remaining, self.app.currency)}"
            )
        )

    def save(self):
        value = self.amount.get().strip()
        if not valid_amount(value):
            return error("Invalid Budget", "Enter a positive budget amount.")

        month = self._selected_month()
        BudgetModel.set_amount(self.app.user_id, month, float(value))

        self.refresh()
        self.app.refresh_all()
        info("Saved", f"Monthly budget saved for {self.month_var.get().split(' (')[0]}.")
