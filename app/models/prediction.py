from datetime import datetime
from app.database import get_db

class PredictionHistory:
    @staticmethod
    def save(data, prediction):
        db = get_db()
        db.execute("""
            INSERT INTO predictions 
            (bedrooms, bathrooms, size, area_avg_price, property_type, area, postcode, predicted_price, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["Bedrooms"], data["Bathrooms"], data["Size"], data["Area_Avg_Price"],
            data["Property Type"], data["Area"], data["Postcode"], prediction,
            datetime.now().isoformat()
        ))
        db.commit()

    @staticmethod
    def get_all():
        db = get_db()
        return db.execute("SELECT * FROM predictions ORDER BY id DESC").fetchall()
