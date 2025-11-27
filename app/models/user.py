import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db

class User:

    @staticmethod
    def create(username, password):
        db = get_db()
        cursor = db.cursor()

        hashed = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )
        db.commit()

    @staticmethod
    def find_by_username(username):
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT id, username, password FROM users WHERE username = ?",
            (username,)
        )
        return cursor.fetchone()

    @staticmethod
    def verify(username, password):
        record = User.find_by_username(username)

        if record is None:
            return None  # User not found

        user_id, username, hashed = record

        if check_password_hash(hashed, password):
            return user_id
        return None
