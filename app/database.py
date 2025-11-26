import sqlite3
from flask import g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("prediction_history.db")
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        # Create users table
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
        """)

        # Create prediction history
        db.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bedrooms REAL,
                bathrooms REAL,
                size REAL,
                area_avg_price REAL,
                property_type TEXT,
                area TEXT,
                postcode TEXT,
                predicted_price REAL,
                timestamp TEXT
            );
        """)

        db.commit()

    app.teardown_appcontext(close_db)
