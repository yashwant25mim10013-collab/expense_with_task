import customtkinter as ctk
from components.header import Header
from components.tables import styled_tree
from components.dialogs import info, error, ask
from models.task_model import TaskModel
from utils.constants import TASK_PRIORITIES, TASK_STATUSES, TASK_CATEGORIES
from utils.date_utils import today_str
from utils.validators import required, valid_date

class TasksPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app=app; self.selected_id=None
        self.grid_columnconfigure(0,weight=1); self.grid_rowconfigure(3,weight=1)
        Header(self,"Task Management").grid(row=0,column=0,sticky="ew",pady=(0,10))

        form=ctk.CTkFrame(self); form.grid(row=1,column=0,sticky="ew")
        for i in range(6): form.grid_columnconfigure(i,weight=1)
        self.title=ctk.CTkEntry(form,placeholder_text="Task title")
        self.due=ctk.CTkEntry(form,placeholder_text="YYYY-MM-DD")
        self.priority=ctk.CTkComboBox(form,values=TASK_PRIORITIES)
        self.category=ctk.CTkComboBox(form,values=TASK_CATEGORIES)
        self.status=ctk.CTkComboBox(form,values=TASK_STATUSES)
        self.desc=ctk.CTkEntry(form,placeholder_text="Description")
        self.due.insert(0,today_str()); self.priority.set("Medium"); self.category.set("Study"); self.status.set("Pending")
        widgets=[self.title,self.due,self.priority,self.category,self.status,self.desc]
        labels=["Title","Due Date","Priority","Category","Status","Description"]
        for i,(l,w) in enumerate(zip(labels,widgets)):
            ctk.CTkLabel(form,text=l).grid(row=0,column=i,padx=5,sticky="w")
            w.grid(row=1,column=i,padx=5,pady=(0,8),sticky="ew")
        ctk.CTkButton(form,text="Save",command=self.save).grid(row=1,column=6,padx=5)

        actions=ctk.CTkFrame(self,fg_color="transparent"); actions.grid(row=2,column=0,sticky="ew",pady=5)
        self.search=ctk.CTkEntry(actions,placeholder_text="Search tasks...")
        self.search.pack(side="left",fill="x",expand=True,padx=(0,8))
        ctk.CTkButton(actions,text="Search",width=100,command=self.refresh).pack(side="left",padx=4)
        ctk.CTkButton(actions,text="Edit Selected",width=120,command=self.load_selected).pack(side="left",padx=4)
        ctk.CTkButton(actions,text="Delete Selected",width=120,command=self.delete).pack(side="left",padx=4)
        ctk.CTkButton(actions,text="Mark Complete",width=130,command=self.complete).pack(side="left",padx=4)

        frame,self.tree=styled_tree(self,
            ("id","title","due","priority","category","status"),
            ("ID","Task","Due Date","Priority","Category","Status"),
            (50,330,110,100,130,120))
        frame.grid(row=3,column=0,sticky="nsew")
        self.refresh()

    def refresh(self):
        for x in self.tree.get_children(): self.tree.delete(x)
        for r in TaskModel.get_all(self.app.user_id, self.search.get().strip() if hasattr(self,"search") else ""):
            self.tree.insert("", "end", values=(r["id"],r["title"],r["due_date"],r["priority"],r["category"],r["status"]))

    def save(self):
        vals=[self.title.get().strip(),self.desc.get().strip(),self.due.get().strip(),self.priority.get(),self.category.get(),self.status.get()]
        if not required(vals[0]): return error("Invalid","Task title is required.")
        if not valid_date(vals[2]): return error("Invalid","Due date must be YYYY-MM-DD.")
        if self.selected_id:
            TaskModel.update(self.app.user_id,self.selected_id,*vals); self.selected_id=None
        else: TaskModel.add(self.app.user_id,*vals)
        self.clear(); self.refresh(); self.app.refresh_all(); info("Saved","Task saved successfully.")

    def selected_row(self):
        sel=self.tree.selection()
        if not sel: info("Select","Select a task first."); return None
        return int(self.tree.item(sel[0])["values"][0])

    def load_selected(self):
        tid=self.selected_row()
        if tid is None: return
        row=next((r for r in TaskModel.get_all(self.app.user_id) if r["id"]==tid),None)
        if row:
            self.selected_id=tid
            self.title.delete(0,"end"); self.title.insert(0,row["title"])
            self.desc.delete(0,"end"); self.desc.insert(0,row["description"] or "")
            self.due.delete(0,"end"); self.due.insert(0,row["due_date"])
            self.priority.set(row["priority"]); self.category.set(row["category"]); self.status.set(row["status"])

    def complete(self):
        tid=self.selected_row()
        if tid is None:return
        row=next((r for r in TaskModel.get_all(self.app.user_id) if r["id"]==tid),None)
        if row:
            TaskModel.update(self.app.user_id,tid,row["title"],row["description"] or "",row["due_date"],row["priority"],row["category"],"Completed")
            self.refresh(); self.app.refresh_all()

    def delete(self):
        tid=self.selected_row()
        if tid is None:return
        if ask("Confirm","Delete selected task?"):
            TaskModel.delete(self.app.user_id,tid); self.refresh(); self.app.refresh_all()

    def clear(self):
        self.title.delete(0,"end"); self.desc.delete(0,"end")
        self.due.delete(0,"end"); self.due.insert(0,today_str())
        self.priority.set("Medium"); self.category.set("Study"); self.status.set("Pending")
