def money(value, currency="₹"):
    try:
        return f"{currency}{float(value):,.2f}"
    except Exception:
        return f"{currency}0.00"

def clear_treeview(tree):
    for item in tree.get_children():
        tree.delete(item)
