
from datetime import datetime
from database.database import get_connection

class TaskModel:
    @staticmethod
    def add(user_id,title,description,due_date,priority,category,status):
        conn=get_connection()
        done=datetime.now().isoformat(timespec="seconds") if status=="Completed" else None
        conn.execute("""INSERT INTO tasks(user_id,title,description,due_date,priority,category,status,created_at,completed_at)
                       VALUES(?,?,?,?,?,?,?,?,?)""",(user_id,title,description,due_date,priority,category,status,datetime.now().isoformat(timespec="seconds"),done))
        conn.commit(); conn.close()

    @staticmethod
    def update(user_id,tid,title,description,due_date,priority,category,status):
        conn=get_connection()
        done=datetime.now().isoformat(timespec="seconds") if status=="Completed" else None
        conn.execute("""UPDATE tasks SET title=?,description=?,due_date=?,priority=?,category=?,status=?,completed_at=?
                       WHERE id=? AND user_id=?""",(title,description,due_date,priority,category,status,done,tid,user_id))
        conn.commit(); conn.close()

    @staticmethod
    def delete(user_id,tid):
        conn=get_connection(); conn.execute("DELETE FROM tasks WHERE id=? AND user_id=?",(tid,user_id)); conn.commit(); conn.close()

    @staticmethod
    def get_all(user_id,search=""):
        conn=get_connection()
        if search:
            r=conn.execute("""SELECT * FROM tasks WHERE user_id=? AND
                (title LIKE ? OR category LIKE ? OR priority LIKE ? OR status LIKE ?)
                ORDER BY due_date ASC,id DESC""",(user_id,f"%{search}%","%"+search+"%","%"+search+"%","%"+search+"%")).fetchall()
        else:
            r=conn.execute("SELECT * FROM tasks WHERE user_id=? ORDER BY due_date ASC,id DESC",(user_id,)).fetchall()
        conn.close(); return r

    @staticmethod
    def counts(user_id):
        conn=get_connection()
        rows=conn.execute("SELECT status,COUNT(*) n FROM tasks WHERE user_id=? GROUP BY status",(user_id,)).fetchall()
        conn.close()
        result={"Pending":0,"In Progress":0,"Completed":0}
        for r in rows: result[r["status"]]=r["n"]
        return result
