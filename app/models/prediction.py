from datetime import datetime
from app.database import get_db

# app/models/prediction.py
class PredictionHistory:
  @staticmethod
  def save(data, prediction):
    price = float(prediction)  # force a real number before insert
    db = get_db()
    db.execute(
      """INSERT INTO predictions
      (bedrooms, bathrooms, size, area_avg_price, property_type, area, postcode, predicted_price, timestamp)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
      (
        data["Bedrooms"], data["Bathrooms"], data["Size"], data["Area_Avg_Price"],
        data["Property Type"], data["Area"], data["Postcode"], price,
        datetime.now().isoformat(),
      ),
    )
    db.commit()

  @staticmethod
  def get_all():
    db = get_db()
    rows = db.execute("SELECT * FROM predictions ORDER BY id DESC").fetchall()

    cleaned = []
    for r in rows:
      raw = r["predicted_price"]
      try:
        price = float(raw) if not isinstance(raw, (bytes, bytearray)) else float(raw.decode("utf-8"))
      except (ValueError, TypeError, UnicodeDecodeError):
        price = None  # skip/flag bad data instead of crashing
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
