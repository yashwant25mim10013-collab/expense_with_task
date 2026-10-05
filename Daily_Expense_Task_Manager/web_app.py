
from flask import Flask, render_template_string, request, redirect, url_for
from database.database import init_db, get_connection
from datetime import date

app=Flask(__name__)
init_db()

HTML="""
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Expense & Task Manager</title>
<style>
body{font-family:Arial;background:#101522;color:#f5f7ff;margin:0;padding:20px}
.wrap{max-width:1000px;margin:auto}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.card{background:#1b2435;padding:18px;border-radius:16px}.accent{color:#63b3ff}input,button{padding:10px;border-radius:8px;border:0;margin:4px}button{background:#5b55e7;color:white}
table{width:100%;border-collapse:collapse}td,th{padding:9px;border-bottom:1px solid #34405a;text-align:left}
</style></head><body><div class="wrap">
<h1> Daily Expense & Task Manager</h1>
<div class="grid">
<div class="card"><small>Today's Expense</small><h2 class="accent">₹{{today}}</h2></div>
<div class="card"><small>Monthly Expense</small><h2>₹{{month}}</h2></div>
<div class="card"><small>Pending Tasks</small><h2>{{pending}}</h2></div>
<div class="card"><small>Budget Remaining</small><h2>₹{{remaining}}</h2></div>
</div>
<h2>Add Expense</h2>
<form method="post" action="/expense">
<input name="amount" placeholder="Amount" required><input name="category" placeholder="Category" value="Food">
<input name="description" placeholder="Description"><button>Add</button></form>
<h2>Recent Expenses</h2><table><tr><th>Date</th><th>Category</th><th>Amount</th><th>Description</th></tr>
{% for r in expenses %}<tr><td>{{r['date']}}</td><td>{{r['category']}}</td><td>₹{{r['amount']}}</td><td>{{r['description']}}</td></tr>{% endfor %}
</table>
<p>For the full desktop experience, run <b>python main.py</b>.</p>
</div></body></html>
"""

@app.route("/")
def home():
    c=get_connection(); uid=c.execute("SELECT id FROM users WHERE username='admin'").fetchone()["id"]
    today=date.today().isoformat(); month=date.today().strftime("%Y-%m")
    today_v=c.execute("SELECT COALESCE(SUM(amount),0) v FROM expenses WHERE user_id=? AND date=?",(uid,today)).fetchone()["v"]
    month_v=c.execute("SELECT COALESCE(SUM(amount),0) v FROM expenses WHERE user_id=? AND substr(date,1,7)=?",(uid,month)).fetchone()["v"]
    pending=c.execute("SELECT COUNT(*) n FROM tasks WHERE user_id=? AND status!='Completed'",(uid,)).fetchone()["n"]
    budget=c.execute("SELECT amount FROM budget WHERE id=1").fetchone()["amount"]
    expenses=c.execute("SELECT * FROM expenses WHERE user_id=? ORDER BY date DESC,id DESC LIMIT 15",(uid,)).fetchall()
    c.close()
    return render_template_string(HTML,today=f"{today_v:,.2f}",month=f"{month_v:,.2f}",pending=pending,remaining=f"{budget-month_v:,.2f}",expenses=expenses)

@app.post("/expense")
def expense():
    amount=float(request.form["amount"]); category=request.form.get("category","Other")
    desc=request.form.get("description",""); c=get_connection()
    uid=c.execute("SELECT id FROM users WHERE username='admin'").fetchone()["id"]
    c.execute("""INSERT INTO expenses(user_id,date,amount,category,description,payment_method,created_at)
                 VALUES(?,?,?,?,?,?,datetime('now'))""",(uid,date.today().isoformat(),amount,category,desc,"Web"))
    c.commit(); c.close(); return redirect(url_for("home"))

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)
