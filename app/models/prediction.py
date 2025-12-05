# app/models/prediction.py

from datetime import datetime
from flask import session
from app.database import get_db

class PredictionHistory:
    @staticmethod
    def save(meta, prediction):

        user_id = session.get("user_id")
        if user_id is None:
            return

        db = get_db()
        db.execute("""
            INSERT INTO predictions
            (mode, location, flat_type, floor_area_sqm, remaining_lease,
            storey_range, address, latitude, longitude,
            predicted_price, price_per_sqm, timestamp, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            meta.get("mode"),
            meta.get("location"),
            meta.get("flat_type"),
            meta.get("floor_area_sqm"),
            meta.get("remaining_lease"),
            meta.get("storey_range"),
            meta.get("address"),
            meta.get("latitude"),
            meta.get("longitude"),
            float(prediction),
            float(meta.get("price_per_sqm")) if meta.get("price_per_sqm") is not None else None,
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
            "price_per_sqm": r["price_per_sqm"],   # NEW FIELD
        } for r in rows]
