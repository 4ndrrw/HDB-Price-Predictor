from datetime import datetime
from app.database import get_db
from app.ml.area_lookup import AREA_AVG_PRICE   # <-- we use the same dict as preprocess.py

class PredictionHistory:
  @staticmethod
  def save(data, prediction):
    """
    Saves prediction results to the database.
    'data' comes from the POST form dictionary.
    """

    # --- Extract required fields ---
    bedrooms = data.get("Bedrooms")
    bathrooms = data.get("Bathrooms")
    size = data.get("Size")
    property_type = data.get("Property Type")
    area = (data.get("Area") or "").strip()
    postcode = data.get("Postcode")
    price = float(prediction)

    # --- Compute Area_Avg_Price from lookup dict ---
    area_avg_price = AREA_AVG_PRICE.get(area)

    # If unknown area (shouldn't happen if user selects from dropdown)
    if area_avg_price is None:
      area_avg_price = 0.0   # or choose to raise an error
      # raise ValueError(f"Unknown area '{area}' — cannot save prediction.")

    # --- DB Insert ---
    db = get_db()
    db.execute(
      """
      INSERT INTO predictions
      (bedrooms, bathrooms, size, area_avg_price, property_type, area, postcode, predicted_price, timestamp)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      """,
      (
        bedrooms,
        bathrooms,
        size,
        area_avg_price,   # <-- no longer crashes
        property_type,
        area,
        postcode,
        price,
        datetime.now().isoformat(),
      ),
    )
    db.commit()

  @staticmethod
  def get_all():
    """
    Fetch + clean prediction history.
    """
    db = get_db()
    rows = db.execute("SELECT * FROM predictions ORDER BY id DESC").fetchall()

    cleaned = []
    for r in rows:
      raw = r["predicted_price"]
      try:
        price = float(raw) if not isinstance(raw, (bytes, bytearray)) else float(raw.decode("utf-8"))
      except (ValueError, TypeError, UnicodeDecodeError):
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
