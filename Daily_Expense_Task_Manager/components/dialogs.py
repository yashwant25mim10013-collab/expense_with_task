from tkinter import messagebox

def info(title, message):
    messagebox.showinfo(title, message)

def error(title, message):
    messagebox.showerror(title, message)

def ask(title, message):
    return messagebox.askyesno(title, message)
