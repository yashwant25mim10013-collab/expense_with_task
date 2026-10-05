import customtkinter as ctk
from components.header import Header
from components.dialogs import info
from database.database import get_connection

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master,fg_color="transparent"); self.app=app
        Header(self,"Settings").pack(anchor="w",pady=(0,20))
        box=ctk.CTkFrame(self); box.pack(fill="x",padx=20)
        ctk.CTkLabel(box,text="Currency").pack(anchor="w",padx=20,pady=(20,5))
        self.currency=ctk.CTkEntry(box); self.currency.insert(0,app.currency); self.currency.pack(fill="x",padx=20)
        ctk.CTkLabel(box,text="Appearance").pack(anchor="w",padx=20,pady=(20,5))
        self.mode=ctk.CTkComboBox(box,values=["System","Light","Dark"]); self.mode.set(app.appearance); self.mode.pack(fill="x",padx=20)
        ctk.CTkButton(box,text="Save Settings",command=self.save).pack(pady=20)

    def save(self):
        self.app.currency=self.currency.get().strip() or "₹"
        self.app.appearance=self.mode.get()
        ctk.set_appearance_mode(self.app.appearance)
        conn=get_connection()
        conn.execute("INSERT INTO settings(key,value) VALUES('currency',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(self.app.currency,))
        conn.commit(); conn.close()
        self.app.refresh_all(); info("Saved","Settings updated.")
