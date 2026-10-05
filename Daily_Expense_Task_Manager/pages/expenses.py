import customtkinter as ctk
from tkinter import ttk
from components.header import Header
from components.tables import styled_tree
from components.dialogs import info, error, ask
from models.expense_model import ExpenseModel
from utils.constants import EXPENSE_CATEGORIES, PAYMENT_METHODS
from utils.date_utils import today_str
from utils.validators import valid_amount, valid_date

class ExpensesPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.selected_id = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        Header(self, "Expense Management").grid(row=0, column=0, sticky="ew", pady=(0,10))

        form = ctk.CTkFrame(self)
        form.grid(row=1, column=0, sticky="ew", pady=5)
        for i in range(6): form.grid_columnconfigure(i, weight=1)

        self.date = ctk.CTkEntry(form, placeholder_text="YYYY-MM-DD")
        self.amount = ctk.CTkEntry(form, placeholder_text="Amount")
        self.category = ctk.CTkComboBox(form, values=EXPENSE_CATEGORIES)
        self.description = ctk.CTkEntry(form, placeholder_text="Description")
        self.payment = ctk.CTkComboBox(form, values=PAYMENT_METHODS)
        self.date.insert(0, today_str())
        self.category.set(EXPENSE_CATEGORIES[0]); self.payment.set(PAYMENT_METHODS[1])

        labels = ["Date","Amount","Category","Description","Payment"]
        widgets = [self.date,self.amount,self.category,self.description,self.payment]
        for i,(l,w) in enumerate(zip(labels,widgets)):
            ctk.CTkLabel(form,text=l).grid(row=0,column=i,padx=5,sticky="w")
            w.grid(row=1,column=i,padx=5,pady=(0,8),sticky="ew")

        ctk.CTkButton(form,text="Save Expense",command=self.save).grid(row=1,column=5,padx=5,sticky="ew")

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=2,column=0,sticky="ew",pady=5)
        self.search = ctk.CTkEntry(actions, placeholder_text="Search category, description...")
        self.search.pack(side="left", fill="x", expand=True, padx=(0,8))
        ctk.CTkButton(actions,text="Search",width=100,command=self.refresh).pack(side="left",padx=4)
        ctk.CTkButton(actions,text="Edit Selected",width=120,command=self.load_selected).pack(side="left",padx=4)
        ctk.CTkButton(actions,text="Delete Selected",width=120,command=self.delete).pack(side="left",padx=4)

        frame, self.tree = styled_tree(self,
            ("id","date","amount","category","description","payment"),
            ("ID","Date","Amount","Category","Description","Payment"),
            (50,110,100,130,280,130))
        frame.grid(row=3,column=0,sticky="nsew")

        self.refresh()

    def refresh(self):
        for x in self.tree.get_children(): self.tree.delete(x)
        for r in ExpenseModel.get_all(self.app.user_id, self.search.get().strip() if hasattr(self,"search") else ""):
            self.tree.insert("", "end", values=(r["id"],r["date"],f'{self.app.currency}{r["amount"]:.2f}',r["category"],r["description"] or "",r["payment_method"]))

    def save(self):
        d,a,c,desc,p = self.date.get().strip(),self.amount.get().strip(),self.category.get(),self.description.get().strip(),self.payment.get()
        if not valid_date(d): return error("Invalid date","Use YYYY-MM-DD.")
        if not valid_amount(a): return error("Invalid amount","Enter a positive amount.")
        if self.selected_id:
            ExpenseModel.update(self.app.user_id,self.selected_id,d,float(a),c,desc,p)
            self.selected_id=None
        else:
            ExpenseModel.add(self.app.user_id,d,float(a),c,desc,p)
        self.clear()
        self.refresh(); self.app.refresh_all(); info("Saved","Expense saved successfully.")

    def load_selected(self):
        sel=self.tree.selection()
        if not sel: return info("Select","Select an expense first.")
        eid=int(self.tree.item(sel[0])["values"][0])
        row=next((r for r in ExpenseModel.get_all(self.app.user_id) if r["id"]==eid),None)
        if row:
            self.selected_id=eid
            for w in [self.date,self.amount,self.description]: w.delete(0,"end")
            self.date.insert(0,row["date"]); self.amount.insert(0,str(row["amount"])); self.description.insert(0,row["description"] or "")
            self.category.set(row["category"]); self.payment.set(row["payment_method"])

    def delete(self):
        sel=self.tree.selection()
        if not sel: return info("Select","Select an expense first.")
        eid=int(self.tree.item(sel[0])["values"][0])
        if ask("Confirm","Delete selected expense?"):
            ExpenseModel.delete(self.app.user_id,eid); self.refresh(); self.app.refresh_all()

    def clear(self):
        self.date.delete(0,"end"); self.date.insert(0,today_str())
        self.amount.delete(0,"end"); self.description.delete(0,"end")
        self.category.set(EXPENSE_CATEGORIES[0]); self.payment.set(PAYMENT_METHODS[1])
