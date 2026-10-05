
from database.database import get_connection

class RecurringModel:
    @staticmethod
    def expenses(user_id):
        c=get_connection(); r=c.execute("SELECT * FROM recurring_expenses WHERE user_id=? ORDER BY next_date",(user_id,)).fetchall(); c.close(); return r
    @staticmethod
    def tasks(user_id):
        c=get_connection(); r=c.execute("SELECT * FROM recurring_tasks WHERE user_id=? ORDER BY next_date",(user_id,)).fetchall(); c.close(); return r
    @staticmethod
    def add_expense(user_id,amount,category,description,payment,frequency,next_date):
        c=get_connection(); c.execute("""INSERT INTO recurring_expenses(user_id,amount,category,description,payment_method,frequency,next_date)
                                         VALUES(?,?,?,?,?,?,?)""",(user_id,amount,category,description,payment,frequency,next_date)); c.commit(); c.close()
    @staticmethod
    def add_task(user_id,title,description,priority,category,frequency,next_date):
        c=get_connection(); c.execute("""INSERT INTO recurring_tasks(user_id,title,description,priority,category,frequency,next_date)
                                         VALUES(?,?,?,?,?,?,?)""",(user_id,title,description,priority,category,frequency,next_date)); c.commit(); c.close()
    @staticmethod
    def toggle(table,rid):
        c=get_connection(); c.execute(f"UPDATE {table} SET active=CASE active WHEN 1 THEN 0 ELSE 1 END WHERE id=?",(rid,)); c.commit(); c.close()
    @staticmethod
    def delete(table,rid):
        c=get_connection(); c.execute(f"DELETE FROM {table} WHERE id=?",(rid,)); c.commit(); c.close()
