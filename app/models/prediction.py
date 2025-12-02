from datetime import datetime
from flask import session
from app.database import get_db


class PredictionHistory:

    @staticmethod
    def save(data, prediction):
        """
        Saves HDB prediction results to the database.
        Works for both BASIC and PRECISE modes.
        Only saves if a user is logged in.
        """

        user_id = session.get("user_id")
        if user_id is None:
            return  # not logged in → no history saved

        # -----------------------------
        # Extract fields from form data
        # -----------------------------
        town = data.get("town")
        street_name = data.get("street_name")      # precise only
        floor_area = data.get("floor_area_sqm")
        flat_type = data.get("flat_type")
        flat_model = data.get("flat_model")        # precise only
        storey_range = data.get("storey_range")    # precise only
        remaining_lease = data.get("remaining_lease")
        address = data.get("address")              # precise only
        mode = data.get("mode", "precise")         # "basic" or "precise"
        price = float(prediction)

        # -----------------------------
        # Insert into DB
        # -----------------------------
        db = get_db()
        db.execute(
            """
            INSERT INTO predictions
            (town, street_name, floor_area_sqm, flat_type, flat_model,
             storey_range, remaining_lease, mode, predicted_price,
             address, timestamp, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                town,
                street_name,
                floor_area,
                flat_type,
                flat_model,
                storey_range,
                remaining_lease,
                mode,
                price,
                address,
                datetime.now().isoformat(),
                user_id
            ),
        )
        db.commit()

    @staticmethod
    def get_all(user_id):
        """
        Returns this user's HDB prediction history formatted for the template.
        """

        if user_id is None:
            return []

        db = get_db()
        rows = db.execute(
            """
            SELECT *
            FROM predictions
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

        cleaned = []
        for r in rows:
            cleaned.append({
                "id": r["id"],
                "town": r["town"],
                "street_name": r["street_name"],
                "floor_area_sqm": r["floor_area_sqm"],
                "flat_type": r["flat_type"],
                "flat_model": r["flat_model"],
                "storey_range": r["storey_range"],
                "remaining_lease": r["remaining_lease"],
                "mode": r["mode"],
                "prediction": r["predicted_price"],
                "address": r["address"],
                "timestamp": r["timestamp"],
            })

        return cleaned
