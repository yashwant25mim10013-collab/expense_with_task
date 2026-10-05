import tkinter as tk
from tkinter import ttk

def styled_tree(master, columns, headings, widths):
    frame = tk.Frame(master)
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=14)
    for col, heading, width in zip(columns, headings, widths):
        tree.heading(col, text=heading)
        tree.column(col, width=width, anchor="center")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return frame, tree
