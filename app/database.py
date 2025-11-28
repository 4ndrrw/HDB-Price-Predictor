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

    # Index on username for faster login lookups
    db.execute("""
CREATE INDEX IF NOT EXISTS idx_users_username
ON users(username);
""")

    # -----------------------------
    # 2. Create prediction history
    # -----------------------------
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

    # Optional index to speed up history queries
    db.execute("""
CREATE INDEX IF NOT EXISTS idx_predictions_timestamp
ON predictions(timestamp);
""")

    # -----------------------------
    # 3. Commit + teardown
    # -----------------------------
    db.commit()

  app.teardown_appcontext(close_db)
