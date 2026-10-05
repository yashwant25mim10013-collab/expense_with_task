import customtkinter as ctk

class Toast(ctk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(master, text=text, corner_radius=10, fg_color=("gray80", "gray20"))
        self.place(relx=0.98, rely=0.96, anchor="se")
        self.after(2200, self.destroy)
