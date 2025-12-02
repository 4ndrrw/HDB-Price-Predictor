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

        db = get_db()
        db.execute("""
            INSERT INTO predictions
            (mode, town, flat_type, floor_area_sqm, remaining_lease,
             street_name, storey_range, flat_model, address,
             latitude, longitude,
             predicted_price, timestamp, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            mode,
            form.get("town"),
            form.get("flat_type"),
            form.get("floor_area_sqm"),
            form.get("remaining_lease"),
            form.get("street_name"),
            form.get("storey_range"),
            form.get("flat_model"),
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

        results = []
        for r in rows:
            results.append({
                "id": r["id"],
                "mode": r["mode"],
                "town": r["town"],
                "flat_type": r["flat_type"],
                "floor_area_sqm": r["floor_area_sqm"],
                "remaining_lease": r["remaining_lease"],
                "street_name": r["street_name"],
                "storey_range": r["storey_range"],
                "flat_model": r["flat_model"],
                "address": r["address"],
                "latitude": r["latitude"],
                "longitude": r["longitude"],
                "predicted_price": r["predicted_price"],
            })

        return results
