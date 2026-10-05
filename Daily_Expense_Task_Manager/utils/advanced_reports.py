
from pathlib import Path
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from models.expense_model import ExpenseModel
from models.task_model import TaskModel
from models.budget_model import BudgetModel
from utils.date_utils import month_range

def create_pdf_report(user_id, display_name):
    out=Path(__file__).resolve().parents[1]/"exports"/"reports"
    out.mkdir(parents=True,exist_ok=True)
    path=out/f"monthly_report_{date.today().strftime('%Y_%m_%d')}.pdf"
    start,end=month_range()
    expenses=ExpenseModel.get_all(user_id)
    tasks=TaskModel.get_all(user_id)
    b=BudgetModel.get()
    total=sum(float(r["amount"]) for r in expenses if start<=r["date"]<=end)
    styles=getSampleStyleSheet()
    doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=15*mm,leftMargin=15*mm,topMargin=15*mm,bottomMargin=15*mm)
    story=[Paragraph("Daily Expense & Task Manager",styles["Title"]),
           Paragraph(f"Monthly Report • {display_name} • {start} to {end}",styles["Normal"]),Spacer(1,8)]
    story.append(Paragraph(f"Total monthly expense: ₹{total:,.2f}",styles["Heading2"]))
    if b: story.append(Paragraph(f"Budget: ₹{float(b['amount']):,.2f} • Remaining: ₹{float(b['amount'])-total:,.2f}",styles["Normal"]))
    story.append(Spacer(1,10))
    data=[["Date","Category","Amount","Description"]]
    for r in expenses:
        if start<=r["date"]<=end: data.append([r["date"],r["category"],f"₹{r['amount']:.2f}",r["description"] or ""])
    table=Table(data,colWidths=[28*mm,35*mm,28*mm,80*mm])
    table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#5145CD")),("TEXTCOLOR",(0,0),(-1,0),colors.white),
                               ("GRID",(0,0),(-1,-1),.4,colors.grey),("FONTSIZE",(0,0),(-1,-1),8),("VALIGN",(0,0),(-1,-1),"TOP")]))
    story += [Paragraph("Expenses",styles["Heading2"]),table,Spacer(1,12),
              Paragraph(f"Tasks: {len(tasks)} total • {sum(1 for t in tasks if t['status']=='Completed')} completed",styles["Heading2"])]
    doc.build(story)
    return path

def backup_database():
    import shutil
    from database.database import DB_PATH
    out=Path(__file__).resolve().parents[1]/"exports"/"reports"
    out.mkdir(parents=True,exist_ok=True)
    path=out/f"backup_{date.today().strftime('%Y_%m_%d')}.db"
    shutil.copy2(DB_PATH,path)
    return path
