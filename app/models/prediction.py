# app/models/prediction.py

from datetime import datetime
from flask import session
from app.database import get_db

class PredictionHistory:
    @staticmethod
    def save(form, prediction):

        user_id = session.get("user_id")
        if user_id is None:
            return

        mode = form.get("mode", "precise")

        # location stored in DB
        location = form.get("location") or form.get("address") or form.get("town")

        db = get_db()
        db.execute("""
            INSERT INTO predictions
            (mode, location, flat_type, floor_area_sqm, remaining_lease,
             storey_range, address, latitude, longitude,
             predicted_price, timestamp, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            mode,
            location,
            form.get("flat_type"),
            form.get("floor_area_sqm"),
            form.get("remaining_lease"),
            form.get("storey_range"),
            form.get("address"),
            form.get("latitude"),
            form.get("longitude"),
            float(prediction),
            datetime.now().isoformat(),
            user_id
        ))

        db.commit()

    @staticmethod
    def get_all(user_id):
        if not user_id:
            return []

        db = get_db()
        rows = db.execute("""
            SELECT *
            FROM predictions
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,)).fetchall()

        return [{
            "id": r["id"],
            "mode": r["mode"],
            "location": r["location"],
            "flat_type": r["flat_type"],
            "floor_area_sqm": r["floor_area_sqm"],
            "remaining_lease": r["remaining_lease"],
            "storey_range": r["storey_range"],
            "address": r["address"],
            "latitude": r["latitude"],
            "longitude": r["longitude"],
            "predicted_price": r["predicted_price"],
        } for r in rows]
