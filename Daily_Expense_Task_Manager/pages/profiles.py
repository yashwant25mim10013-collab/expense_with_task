
import customtkinter as ctk
from components.header import Header
from models.user_model import UserModel

class ProfilesPage(ctk.CTkFrame):
    def __init__(self,master,app):
        super().__init__(master,fg_color="transparent"); self.app=app
        Header(self,"👤 Profiles").pack(anchor="w",pady=(0,15))
        ctk.CTkLabel(self,text=f"Logged in as: {app.display_name}",font=ctk.CTkFont(size=18,weight="bold")).pack(anchor="w")
        self.box=ctk.CTkTextbox(self,height=400); self.box.pack(fill="both",expand=True,pady=15)
        self.refresh()
    def refresh(self):
        self.box.delete("1.0","end")
        for r in UserModel.all_users():
            self.box.insert("end",f'#{r["id"]}  {r["username"]}  |  {r["display_name"]}  | created {r["created_at"][:10]}\n')
