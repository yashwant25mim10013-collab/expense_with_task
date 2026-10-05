
import customtkinter as ctk
from tkinter import messagebox
from components.header import Header
from models.recurring_model import RecurringModel
from utils.constants import EXPENSE_CATEGORIES,PAYMENT_METHODS,TASK_PRIORITIES,TASK_CATEGORIES
from utils.validators import valid_amount,valid_date

class RecurringPage(ctk.CTkFrame):
    def __init__(self,master,app):
        super().__init__(master,fg_color="transparent"); self.app=app
        self.grid_columnconfigure((0,1),weight=1)
        Header(self,"Recurring Automation").grid(row=0,column=0,columnspan=2,sticky="ew",pady=(0,12))
        self.exp_box=ctk.CTkFrame(self); self.exp_box.grid(row=1,column=0,sticky="nsew",padx=5)
        self.task_box=ctk.CTkFrame(self); self.task_box.grid(row=1,column=1,sticky="nsew",padx=5)
        self.build_expense(); self.build_task()
    def build_expense(self):
        b=self.exp_box; ctk.CTkLabel(b,text="Recurring Expenses",font=ctk.CTkFont(size=18,weight="bold")).pack(pady=12)
        self.e_amt=ctk.CTkEntry(b,placeholder_text="Amount"); self.e_amt.pack(padx=20,pady=5,fill="x")
        self.e_cat=ctk.CTkComboBox(b,values=EXPENSE_CATEGORIES); self.e_cat.set("Food"); self.e_cat.pack(padx=20,pady=5,fill="x")
        self.e_desc=ctk.CTkEntry(b,placeholder_text="Description"); self.e_desc.pack(padx=20,pady=5,fill="x")
        self.e_pay=ctk.CTkComboBox(b,values=PAYMENT_METHODS); self.e_pay.set("UPI"); self.e_pay.pack(padx=20,pady=5,fill="x")
        self.e_freq=ctk.CTkComboBox(b,values=["Daily","Weekly","Monthly"]); self.e_freq.set("Monthly"); self.e_freq.pack(padx=20,pady=5,fill="x")
        self.e_date=ctk.CTkEntry(b,placeholder_text="First date YYYY-MM-DD"); self.e_date.pack(padx=20,pady=5,fill="x")
        ctk.CTkButton(b,text="Add Recurring Expense",command=self.add_expense).pack(pady=8)
        self.elist=ctk.CTkTextbox(b,height=170); self.elist.pack(fill="both",expand=True,padx=15,pady=10)
    def build_task(self):
        b=self.task_box; ctk.CTkLabel(b,text="Recurring Tasks",font=ctk.CTkFont(size=18,weight="bold")).pack(pady=12)
        self.t_title=ctk.CTkEntry(b,placeholder_text="Task title"); self.t_title.pack(padx=20,pady=5,fill="x")
        self.t_desc=ctk.CTkEntry(b,placeholder_text="Description"); self.t_desc.pack(padx=20,pady=5,fill="x")
        self.t_pri=ctk.CTkComboBox(b,values=TASK_PRIORITIES); self.t_pri.set("Medium"); self.t_pri.pack(padx=20,pady=5,fill="x")
        self.t_cat=ctk.CTkComboBox(b,values=TASK_CATEGORIES); self.t_cat.set("Study"); self.t_cat.pack(padx=20,pady=5,fill="x")
        self.t_freq=ctk.CTkComboBox(b,values=["Daily","Weekly","Monthly"]); self.t_freq.set("Weekly"); self.t_freq.pack(padx=20,pady=5,fill="x")
        self.t_date=ctk.CTkEntry(b,placeholder_text="First date YYYY-MM-DD"); self.t_date.pack(padx=20,pady=5,fill="x")
        ctk.CTkButton(b,text="Add Recurring Task",command=self.add_task).pack(pady=8)
        self.tlist=ctk.CTkTextbox(b,height=170); self.tlist.pack(fill="both",expand=True,padx=15,pady=10)
        self.refresh()
    def add_expense(self):
        if not valid_amount(self.e_amt.get()) or not valid_date(self.e_date.get()): return messagebox.showerror("Invalid","Enter positive amount and valid date.")
        RecurringModel.add_expense(self.app.user_id,float(self.e_amt.get()),self.e_cat.get(),self.e_desc.get(),self.e_pay.get(),self.e_freq.get(),self.e_date.get()); self.refresh()
    def add_task(self):
        if not self.t_title.get().strip() or not valid_date(self.t_date.get()): return messagebox.showerror("Invalid","Enter title and valid date.")
        RecurringModel.add_task(self.app.user_id,self.t_title.get(),self.t_desc.get(),self.t_pri.get(),self.t_cat.get(),self.t_freq.get(),self.t_date.get()); self.refresh()
    def refresh(self):
        if not hasattr(self,"elist"): return
        self.elist.delete("1.0","end"); self.tlist.delete("1.0","end")
        for r in RecurringModel.expenses(self.app.user_id):
            self.elist.insert("end",f'#{r["id"]} {r["frequency"]} | {r["category"]} | ₹{r["amount"]:.2f} | next: {r["next_date"]} | {"ON" if r["active"] else "OFF"}\n')
        for r in RecurringModel.tasks(self.app.user_id):
            self.tlist.insert("end",f'#{r["id"]} {r["frequency"]} | {r["title"]} | next: {r["next_date"]} | {"ON" if r["active"] else "OFF"}\n')
