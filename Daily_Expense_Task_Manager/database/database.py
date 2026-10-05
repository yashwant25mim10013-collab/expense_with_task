
import sqlite3
from pathlib import Path
from datetime import datetime, date, timedelta
import hashlib

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "expense_task.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        display_name TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        payment_method TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT NOT NULL,
        priority TEXT NOT NULL,
        category TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        completed_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS budget(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        month TEXT NOT NULL,
        UNIQUE(user_id, month),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS settings(
        key TEXT PRIMARY KEY,
        value TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS login_sessions(
        id INTEGER PRIMARY KEY CHECK (id = 1),
        user_id INTEGER NOT NULL,
        token_hash TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS recurring_expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        payment_method TEXT NOT NULL,
        frequency TEXT NOT NULL,
        next_date TEXT NOT NULL,
        active INTEGER DEFAULT 1,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS recurring_tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        priority TEXT NOT NULL,
        category TEXT NOT NULL,
        frequency TEXT NOT NULL,
        next_date TEXT NOT NULL,
        active INTEGER DEFAULT 1,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS reminders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        message TEXT,
        remind_at TEXT NOT NULL,
        done INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")

    # Add user_id columns to older databases if necessary
    for table in ("expenses", "tasks", "recurring_expenses", "recurring_tasks", "reminders"):
        try:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN user_id INTEGER")
        except sqlite3.OperationalError:
            pass

    # Default demo account
    demo_hash = hash_password("admin123")
    cur.execute("INSERT OR IGNORE INTO users(username,password_hash,display_name,created_at) VALUES(?,?,?,?)",
                ("admin", demo_hash, "Demo User", datetime.now().isoformat(timespec="seconds")))

    # Migrate the old single/global budget table to per-user, per-month budgets.
    budget_columns = [r["name"] for r in cur.execute("PRAGMA table_info(budget)").fetchall()]
    if "user_id" not in budget_columns:
        cur.execute("ALTER TABLE budget RENAME TO budget_old")
        cur.execute("""CREATE TABLE budget(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL,
            UNIQUE(user_id, month),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )""")
        old_rows = cur.execute("SELECT amount, month FROM budget_old").fetchall()
        admin = cur.execute("SELECT id FROM users WHERE username='admin'").fetchone()
        if admin:
            for row in old_rows:
                cur.execute(
                    "INSERT OR IGNORE INTO budget(user_id,amount,month) VALUES(?,?,?)",
                    (admin["id"], row["amount"], row["month"])
                )
        cur.execute("DROP TABLE budget_old")

    # New installations start with a sensible demo budget for the demo account.
    demo_user = cur.execute("SELECT id FROM users WHERE username='admin'").fetchone()
    if demo_user and cur.execute(
        "SELECT COUNT(*) FROM budget WHERE user_id=?",
        (demo_user["id"],)
    ).fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO budget(user_id,amount,month) VALUES(?,?,?)",
            (demo_user["id"], 10000, date.today().strftime("%Y-%m"))
        )

    conn.commit()
    conn.close()

def seed_sample_data():
    conn = get_connection()
    uid = conn.execute("SELECT id FROM users WHERE username='admin'").fetchone()["id"]
    now = datetime.now().isoformat(timespec="seconds")

    if conn.execute("SELECT COUNT(*) FROM expenses WHERE user_id=?", (uid,)).fetchone()[0] == 0:
        rows = [
            (uid,date.today().isoformat(),150,"Food","Lunch","UPI",now),
            (uid,date.today().isoformat(),50,"Transport","Bus","Cash",now),
            (uid,date.today().isoformat(),250,"Education","Books","UPI",now)
        ]
        conn.executemany("""INSERT INTO expenses(user_id,date,amount,category,description,payment_method,created_at)
                            VALUES(?,?,?,?,?,?,?)""", rows)

    if conn.execute("SELECT COUNT(*) FROM tasks WHERE user_id=?", (uid,)).fetchone()[0] == 0:
        rows = [
            (uid,"Complete DSA revision","Revise trees and graphs",date.today().isoformat(),"High","Study","Pending",now,None),
            (uid,"Practice Python","Work on Tkinter project",date.today().isoformat(),"Medium","Project","In Progress",now,None),
            (uid,"Submit assignment","Check final PDF",date.today().isoformat(),"High","College","Completed",now,now)
        ]
        conn.executemany("""INSERT INTO tasks(user_id,title,description,due_date,priority,category,status,created_at,completed_at)
                            VALUES(?,?,?,?,?,?,?,?,?)""", rows)

    conn.commit()
    conn.close()

def advance_date(current, frequency):
    d = date.fromisoformat(current)
    if frequency == "Daily":
        d += timedelta(days=1)
    elif frequency == "Weekly":
        d += timedelta(weeks=1)
    elif frequency == "Monthly":
        month = d.month + 1
        year = d.year + (month-1)//12
        month = (month-1)%12 + 1
        import calendar
        day = min(d.day, calendar.monthrange(year, month)[1])
        d = date(year, month, day)
    return d.isoformat()

def process_recurring_items(user_id):
    conn = get_connection()
    today = date.today().isoformat()

    expenses = conn.execute("SELECT * FROM recurring_expenses WHERE user_id=? AND active=1 AND next_date<=?",
                            (user_id,today)).fetchall()
    for r in expenses:
        next_date = r["next_date"]
        while next_date <= today:
            conn.execute("""INSERT INTO expenses(user_id,date,amount,category,description,payment_method,created_at)
                            VALUES(?,?,?,?,?,?,?)""",
                         (user_id,next_date,r["amount"],r["category"],r["description"],
                          r["payment_method"],datetime.now().isoformat(timespec="seconds")))
            next_date = advance_date(next_date,r["frequency"])
        conn.execute("UPDATE recurring_expenses SET next_date=? WHERE id=?", (next_date,r["id"]))

    tasks = conn.execute("SELECT * FROM recurring_tasks WHERE user_id=? AND active=1 AND next_date<=?",
                         (user_id,today)).fetchall()
    for r in tasks:
        next_date = r["next_date"]
        while next_date <= today:
            conn.execute("""INSERT INTO tasks(user_id,title,description,due_date,priority,category,status,created_at)
                            VALUES(?,?,?,?,?,?,?,?)""",
                         (user_id,r["title"],r["description"],next_date,r["priority"],r["category"],"Pending",
                          datetime.now().isoformat(timespec="seconds")))
            next_date = advance_date(next_date,r["frequency"])
        conn.execute("UPDATE recurring_tasks SET next_date=? WHERE id=?", (next_date,r["id"]))

    conn.commit()
    conn.close()
