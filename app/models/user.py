from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db

class User:
    @staticmethod
    def create(username, password):
        db = get_db()
        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                   (username, password_hash))
        db.commit()

    @staticmethod
    def authenticate(username, password):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            return True
        return False
