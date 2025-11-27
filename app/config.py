import os

class Config:
    SECRET_KEY = "supersecret31415926535897"
    DATABASE = os.path.join(os.getcwd(), "prediction_history.db")
