
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database.database import get_connection

class RemindersPage(ctk.CTkFrame):
    def __init__(self,master,app):
        super().__init__(master,fg_color="transparent"); self.app=app
        ctk.CTkLabel(self,text="⏰ Reminders",font=ctk.CTkFont(size=24,weight="bold")).pack(anchor="w",pady=(0,15))
        self.title=ctk.CTkEntry(self,placeholder_text="Reminder title"); self.title.pack(fill="x",pady=5)
        self.msg=ctk.CTkEntry(self,placeholder_text="Message"); self.msg.pack(fill="x",pady=5)
        self.when=ctk.CTkEntry(self,placeholder_text="YYYY-MM-DD HH:MM"); self.when.pack(fill="x",pady=5)
        ctk.CTkButton(self,text="Add Reminder",command=self.add).pack(pady=8)
        self.list=ctk.CTkTextbox(self,height=350); self.list.pack(fill="both",expand=True,pady=10)
        self.refresh()
    def add(self):
        try: datetime.strptime(self.when.get(),"%Y-%m-%d %H:%M")
        except ValueError: return messagebox.showerror("Invalid","Use YYYY-MM-DD HH:MM")
        c=get_connection(); c.execute("INSERT INTO reminders(user_id,title,message,remind_at) VALUES(?,?,?,?)",
            (self.app.user_id,self.title.get(),self.msg.get(),self.when.get())); c.commit(); c.close()
        self.title.delete(0,"end"); self.msg.delete(0,"end"); self.when.delete(0,"end"); self.refresh()
    def refresh(self):
        c=get_connection(); rows=c.execute("SELECT * FROM reminders WHERE user_id=? ORDER BY remind_at",(self.app.user_id,)).fetchall(); c.close()
        self.list.delete("1.0","end")
        for r in rows: self.list.insert("end",f'#{r["id"]} | {r["remind_at"]} | {r["title"]} | {"Done" if r["done"] else "Pending"}\n')
