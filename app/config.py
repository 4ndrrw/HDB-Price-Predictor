import os
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    DATABASE = os.path.join(os.getcwd(), "prediction_history.db")
