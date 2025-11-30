from datetime import datetime
from flask import session
from app.database import get_db
from app.ml.area_lookup import AREA_AVG_PRICE   # <-- we use the same dict as preprocess.py


class PredictionHistory:

    @staticmethod
    def save(data, prediction):
        """
        Saves prediction results to the database.
        Only saves if a user is logged in.
        """

        # ---------------------------------------
        # Check login state
        # ---------------------------------------
        user_id = session.get("user_id")
        if user_id is None:
            # Not logged in → do not record history
            return

        # --- Extract required fields ---
        bedrooms = data.get("Bedrooms")
        bathrooms = data.get("Bathrooms")
        size = data.get("Size")
        property_type = data.get("Property Type")
        area = (data.get("Area") or "").strip()
        postcode = data.get("Postcode")
        price = float(prediction)

        # --- Compute Area_Avg_Price ---
        area_avg_price = AREA_AVG_PRICE.get(area, 0.0)

        # --- DB Insert (including user_id) ---
        db = get_db()
        db.execute(
            """
            INSERT INTO predictions
            (bedrooms, bathrooms, size, area_avg_price, property_type, area,
             postcode, predicted_price, timestamp, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                bedrooms,
                bathrooms,
                size,
                area_avg_price,
                property_type,
                area,
                postcode,
                price,
                datetime.now().isoformat(),
                user_id,
            ),
        )
        db.commit()

    @staticmethod
    def get_all(user_id):
        """
        Return prediction history ONLY for this user.
        If user_id is None → return empty list.
        """

        if user_id is None:
            return []  # logged-out → no history shown

        db = get_db()
        rows = db.execute(
            """
            SELECT * FROM predictions
            WHERE user_id = ?
            ORDER BY id ASC
            """,
            (user_id,),
        ).fetchall()

        cleaned = []
        for r in rows:
            raw = r["predicted_price"]
            try:
                if isinstance(raw, (bytes, bytearray)):
                    price = float(raw.decode("utf-8"))
                else:
                    price = float(raw)
            except Exception:
                price = None

            cleaned.append({
                "id": r["id"],
                "property_type": r["property_type"],
                "bedrooms": r["bedrooms"],
                "bathrooms": r["bathrooms"],
                "size": r["size"],
                "postcode": r["postcode"],
                "predicted_price": price,
            })

        return cleaned
