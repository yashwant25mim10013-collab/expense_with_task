from database.database import get_connection

class BudgetModel:
    @staticmethod
    def get(user_id, month):
        c = get_connection()
        r = c.execute(
            "SELECT * FROM budget WHERE user_id=? AND month=?",
            (user_id, month)
        ).fetchone()
        c.close()
        return r

    @staticmethod
    def set_amount(user_id, month, amount):
        c = get_connection()
        c.execute(
            """INSERT INTO budget(user_id, amount, month)
               VALUES(?,?,?)
               ON CONFLICT(user_id, month)
               DO UPDATE SET amount=excluded.amount""",
            (user_id, amount, month)
        )
        c.commit()
        c.close()
