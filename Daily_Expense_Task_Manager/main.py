
import customtkinter as ctk
from database.database import init_db,seed_sample_data,process_recurring_items,get_connection
from components.sidebar import Sidebar
from pages.login import LoginPage
from pages.dashboard import DashboardPage
from pages.expenses import ExpensesPage
from pages.tasks import TasksPage
from pages.analytics import AnalyticsPage
from pages.budget import BudgetPage
from pages.reports import ReportsPage
from pages.settings import SettingsPage
from pages.recurring import RecurringPage
from pages.reminders import RemindersPage
from pages.insights import InsightsPage
from pages.profiles import ProfilesPage

class App(ctk.CTk):
    def __init__(self,user):
        super().__init__()
        self.user_id=user["id"]; self.display_name=user["display_name"]
        self.currency="₹"; self.appearance="System"
        self.title("Daily Expense & Task Manager")
        self.geometry("1300x800"); self.minsize(1050,680)
        self.load_settings()
        ctk.set_appearance_mode(self.appearance); ctk.set_default_color_theme("blue")
        self.grid_columnconfigure(1,weight=1); self.grid_rowconfigure(0,weight=1)
        self.sidebar=Sidebar(self,self.show_page, self.logout); self.sidebar.grid(row=0,column=0,sticky="nsew")
        self.content=ctk.CTkFrame(self,corner_radius=0,fg_color="transparent")
        self.content.grid(row=0,column=1,sticky="nsew",padx=20,pady=20)
        self.content.grid_rowconfigure(0,weight=1); self.content.grid_columnconfigure(0,weight=1)
        self.pages={}
        self.page_classes={
            "Dashboard":DashboardPage,"Expenses":ExpensesPage,"Tasks":TasksPage,"Analytics":AnalyticsPage,
            "Budget":BudgetPage,"Reports":ReportsPage,"Settings":SettingsPage,"Recurring":RecurringPage,
            "Reminders":RemindersPage,"Smart Insights":InsightsPage,"Profiles":ProfilesPage
        }
        self.show_page("Dashboard")
        process_recurring_items(self.user_id)
        self.after(60000,self.check_reminders)

    def logout(self):
        from tkinter import messagebox
        if messagebox.askyesno("Logout", "Logout this user on this computer?\nYou can login again later."):
            from models.user_model import UserModel
            UserModel.clear_session()
            self.destroy()
            start()

    def load_settings(self):
        c=get_connection()
        for r in c.execute("SELECT key,value FROM settings").fetchall():
            if r["key"]=="currency": self.currency=r["value"]
        c.close()

    def show_page(self,name):
        for p in self.pages.values(): p.grid_forget()
        if name not in self.pages: self.pages[name]=self.page_classes[name](self.content,self)
        p=self.pages[name]; p.grid(row=0,column=0,sticky="nsew")
        if hasattr(p,"refresh"):
            try:p.refresh()
            except Exception:pass

    def refresh_all(self):
        for p in self.pages.values():
            if hasattr(p,"refresh"):
                try:p.refresh()
                except Exception:pass

    def check_reminders(self):
        from datetime import datetime
        c=get_connection()
        now=datetime.now().strftime("%Y-%m-%d %H:%M")
        rows=c.execute("SELECT * FROM reminders WHERE user_id=? AND done=0 AND remind_at<=?",(self.user_id,now)).fetchall()
        for r in rows:
            c.execute("UPDATE reminders SET done=1 WHERE id=?",(r["id"],))
            try:
                from tkinter import messagebox
                messagebox.showinfo("⏰ Reminder",f'{r["title"]}\n{r["message"] or ""}')
            except Exception: pass
        c.commit(); c.close()
        process_recurring_items(self.user_id)
        self.refresh_all()
        self.after(60000,self.check_reminders)

def start():
    init_db(); seed_sample_data()
    remembered_user = __import__("models.user_model", fromlist=["UserModel"]).UserModel.get_remembered_user()
    if remembered_user:
        app=App(remembered_user); app.mainloop(); return
    root=ctk.CTk(); root.title("Login"); root.geometry("700x600")
    root.minsize(600,500)
    login=LoginPage(root,lambda user: launch(root,user)); login.pack(fill="both",expand=True)
    root.mainloop()

def launch(login_root,user):
    login_root.destroy()
    app=App(user); app.mainloop()

if __name__=="__main__":
    start()
