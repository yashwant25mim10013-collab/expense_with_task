
import customtkinter as ctk
from tkinter import messagebox
from models.user_model import UserModel

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, on_login):
        super().__init__(master, fg_color="transparent")
        self.on_login=on_login
        box=ctk.CTkFrame(self,corner_radius=18,width=420,height=430)
        box.place(relx=.5,rely=.5,anchor="center")
        ctk.CTkLabel(box,text="💰",font=ctk.CTkFont(size=48)).pack(pady=(35,0))
        ctk.CTkLabel(box,text="Daily Expense & Task Manager",font=ctk.CTkFont(size=22,weight="bold")).pack(pady=8)
        ctk.CTkLabel(box,text="Sign in to continue",text_color="gray").pack(pady=(0,20))
        self.user=ctk.CTkEntry(box,placeholder_text="Username",width=300); self.user.pack(pady=8)
        self.pwd=ctk.CTkEntry(box,placeholder_text="Password",show="*",width=300); self.pwd.pack(pady=8)
        self.remember=ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(box,text="Remember me on this computer",variable=self.remember).pack(pady=(2,8))
        ctk.CTkButton(box,text="Login",width=300,height=40,command=self.login).pack(pady=10)
        ctk.CTkLabel(box,text="Demo: admin / admin123",text_color="gray").pack(pady=5)
        ctk.CTkButton(box,text="Create New Profile",fg_color="transparent",command=self.register).pack(pady=5)
    def login(self):
        r=UserModel.authenticate(self.user.get().strip(),self.pwd.get())
        if r:
            if self.remember.get():
                UserModel.remember_session(r["id"])
            else:
                UserModel.clear_session()
            self.on_login(r)
        else: messagebox.showerror("Login Failed","Invalid username or password.")
    def register(self):
        win=ctk.CTkToplevel(self); win.title("Create Profile"); win.geometry("420x360"); win.grab_set()
        fields=[]
        for ph in ["Display name","Username","Password"]:
            e=ctk.CTkEntry(win,placeholder_text=ph,show="*" if ph=="Password" else None,width=300); e.pack(pady=12); fields.append(e)
        def create():
            if not all(e.get().strip() for e in fields):
                return messagebox.showerror("Error","All fields are required.")
            if UserModel.create(fields[1].get().strip(),fields[2].get(),fields[0].get().strip()):
                messagebox.showinfo("Success","Profile created. You can now login."); win.destroy()
            else: messagebox.showerror("Error","Username already exists.")
        ctk.CTkButton(win,text="Create Profile",command=create).pack(pady=15)
