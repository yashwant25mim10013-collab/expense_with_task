
import customtkinter as ctk
from components.header import Header
from analytics.ai_insights import generate_insights

class InsightsPage(ctk.CTkFrame):
    def __init__(self,master,app):
        super().__init__(master,fg_color="transparent"); self.app=app
        Header(self,"🤖 Smart Insights").pack(anchor="w",pady=(0,15))
        ctk.CTkLabel(self,text="Local AI-style analysis of your data",text_color="gray").pack(anchor="w")
        self.box=ctk.CTkTextbox(self,height=430); self.box.pack(fill="both",expand=True,pady=15)
        self.refresh()
    def refresh(self):
        self.box.configure(state="normal"); self.box.delete("1.0","end")
        for i,text in enumerate(generate_insights(self.app.user_id),1):
            self.box.insert("end",f"{i}. {text}\n\n")
        self.box.configure(state="disabled")
