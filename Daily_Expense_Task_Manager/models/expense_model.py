
from datetime import datetime
from database.database import get_connection

class ExpenseModel:
    @staticmethod
    def add(user_id,date,amount,category,description,payment_method):
        conn=get_connection()
        conn.execute("""INSERT INTO expenses(user_id,date,amount,category,description,payment_method,created_at)
                       VALUES(?,?,?,?,?,?,?)""",(user_id,date,amount,category,description,payment_method,datetime.now().isoformat(timespec="seconds")))
        conn.commit(); conn.close()

    @staticmethod
    def update(user_id,eid,date,amount,category,description,payment_method):
        conn=get_connection()
        conn.execute("""UPDATE expenses SET date=?,amount=?,category=?,description=?,payment_method=?
                       WHERE id=? AND user_id=?""",(date,amount,category,description,payment_method,eid,user_id))
        conn.commit(); conn.close()

    @staticmethod
    def delete(user_id,eid):
        conn=get_connection(); conn.execute("DELETE FROM expenses WHERE id=? AND user_id=?",(eid,user_id)); conn.commit(); conn.close()

    @staticmethod
    def get_all(user_id,search=""):
        conn=get_connection()
        if search:
            rows=conn.execute("""SELECT * FROM expenses WHERE user_id=? AND
                (category LIKE ? OR description LIKE ? OR payment_method LIKE ?)
                ORDER BY date DESC,id DESC""",(user_id,f"%{search}%",f"%{search}%",f"%{search}%")).fetchall()
        else:
            rows=conn.execute("SELECT * FROM expenses WHERE user_id=? ORDER BY date DESC,id DESC",(user_id,)).fetchall()
        conn.close(); return rows

    @staticmethod
    def total_between(user_id,start,end):
        conn=get_connection()
        v=conn.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE user_id=? AND date BETWEEN ? AND ?",
                       (user_id,start,end)).fetchone()[0]
        conn.close(); return float(v or 0)

    @staticmethod
    def category_totals(user_id,start,end):
        conn=get_connection()
        r=conn.execute("""SELECT category,SUM(amount) total FROM expenses
                          WHERE user_id=? AND date BETWEEN ? AND ? GROUP BY category ORDER BY total DESC""",
                       (user_id,start,end)).fetchall()
        conn.close(); return r

    @staticmethod
    def daily_totals(user_id,start,end):
        conn=get_connection()
        r=conn.execute("""SELECT date,SUM(amount) total FROM expenses
                          WHERE user_id=? AND date BETWEEN ? AND ? GROUP BY date ORDER BY date""",
                       (user_id,start,end)).fetchall()
        conn.close(); return r
