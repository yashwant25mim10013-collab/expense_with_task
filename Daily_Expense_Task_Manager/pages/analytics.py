import customtkinter as ctk
from datetime import date, timedelta
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from components.header import Header
from analytics.expense_analytics import summary

class AnalyticsPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master,fg_color="transparent")
        self.app=app
        self.grid_columnconfigure((0,1),weight=1); self.grid_rowconfigure(1,weight=1)
        Header(self,"Analytics").grid(row=0,column=0,columnspan=2,sticky="ew",pady=(0,10))
        self.left=ctk.CTkFrame(self); self.right=ctk.CTkFrame(self)
        self.left.grid(row=1,column=0,sticky="nsew",padx=5); self.right.grid(row=1,column=1,sticky="nsew",padx=5)
        self.refresh()

    def refresh(self):
        for w in self.left.winfo_children(): w.destroy()
        for w in self.right.winfo_children(): w.destroy()
        data=summary(self.app.user_id)

        fig1=Figure(figsize=(5,4),dpi=90); ax1=fig1.add_subplot(111)
        cats=[r["category"] for r in data["categories"]]; vals=[r["total"] for r in data["categories"]]
        if vals: ax1.pie(vals,labels=cats,autopct="%1.0f%%")
        else: ax1.text(.5,.5,"No expense data",ha="center",va="center")
        ax1.set_title("Spending by Category")
        FigureCanvasTkAgg(fig1,master=self.left).get_tk_widget().pack(fill="both",expand=True)

        fig2=Figure(figsize=(5,4),dpi=90); ax2=fig2.add_subplot(111)
        dates=[r["date"][-2:] for r in data["daily"]]; vals=[r["total"] for r in data["daily"]]
        ax2.bar(dates,vals)
        ax2.set_title("Daily Spending - Current Month"); ax2.set_xlabel("Day"); ax2.set_ylabel("Amount")
        FigureCanvasTkAgg(fig2,master=self.right).get_tk_widget().pack(fill="both",expand=True)
