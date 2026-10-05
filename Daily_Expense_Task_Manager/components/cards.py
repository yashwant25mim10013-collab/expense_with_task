import customtkinter as ctk

class StatCard(ctk.CTkFrame):
    def __init__(self, master, title, value, icon=""):
        super().__init__(master, corner_radius=14)
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text=f"{icon}  {title}", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, padx=18, pady=(14, 4), sticky="w")
        self.value_label = ctk.CTkLabel(self, text=value, font=ctk.CTkFont(size=25, weight="bold"))
        self.value_label.grid(row=1, column=0, padx=18, pady=(0, 14), sticky="w")

    def set_value(self, value):
        self.value_label.configure(text=value)
