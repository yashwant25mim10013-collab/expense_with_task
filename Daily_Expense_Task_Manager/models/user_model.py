from datetime import datetime
import hashlib
import secrets
from pathlib import Path
from database.database import get_connection, hash_password

SESSION_FILE = Path.home() / ".daily_expense_manager_session"

class UserModel:
    @staticmethod
    def authenticate(username,password):
        c=get_connection()
        r=c.execute("SELECT * FROM users WHERE username=? AND password_hash=?",
                    (username,hash_password(password))).fetchone()
        c.close(); return r

    @staticmethod
    def create(username,password,display_name):
        c=get_connection()
        try:
            c.execute("INSERT INTO users(username,password_hash,display_name,created_at) VALUES(?,?,?,?)",
                      (username,hash_password(password),display_name,datetime.now().isoformat(timespec="seconds")))
            c.commit(); return True
        except Exception: return False
        finally: c.close()

    @staticmethod
    def all_users():
        c=get_connection(); r=c.execute("SELECT id,username,display_name,created_at FROM users ORDER BY id").fetchall(); c.close(); return r

    @staticmethod
    def remember_session(user_id):
        token=secrets.token_urlsafe(32)
        token_hash=hashlib.sha256(token.encode("utf-8")).hexdigest()
        c=get_connection()
        c.execute("INSERT INTO login_sessions(id,user_id,token_hash,created_at) VALUES(1,?,?,?) "
                  "ON CONFLICT(id) DO UPDATE SET user_id=excluded.user_id, token_hash=excluded.token_hash, created_at=excluded.created_at",
                  (user_id,token_hash,datetime.now().isoformat(timespec="seconds")))
        c.commit(); c.close()
        try:
            SESSION_FILE.write_text(token, encoding="utf-8")
        except OSError:
            pass

    @staticmethod
    def get_remembered_user():
        try:
            token=SESSION_FILE.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError):
            return None
        if not token:
            return None
        token_hash=hashlib.sha256(token.encode("utf-8")).hexdigest()
        c=get_connection()
        r=c.execute("SELECT u.* FROM users u JOIN login_sessions s ON s.user_id=u.id "
                    "WHERE s.id=1 AND s.token_hash=?",(token_hash,)).fetchone()
        c.close()
        return r

    @staticmethod
    def clear_session():
        c=get_connection(); c.execute("DELETE FROM login_sessions WHERE id=1"); c.commit(); c.close()
        try:
            SESSION_FILE.unlink()
        except OSError:
            pass
