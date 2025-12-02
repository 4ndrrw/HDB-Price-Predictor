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

        # -----------------------------
        # 1. Create users table
        # -----------------------------
        db.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

        db.execute("""
CREATE INDEX IF NOT EXISTS idx_users_username
ON users(username);
""")

        # -----------------------------
        # 2. Create prediction history (HDB version)
        # -----------------------------
        db.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- COMMON FIELDS
    mode TEXT,

    -- BASIC MODE
    town TEXT,
    flat_type TEXT,
    floor_area_sqm REAL,
    remaining_lease REAL,

    -- PRECISE MODE
    street_name TEXT,
    storey_range TEXT,
    address TEXT,
    latitude REAL,
    longitude REAL,

    predicted_price REAL,
    timestamp TEXT,
    user_id INTEGER
);
""")

        db.execute("""
CREATE INDEX IF NOT EXISTS idx_predictions_timestamp
ON predictions(timestamp);
""")

        db.commit()

    app.teardown_appcontext(close_db)
