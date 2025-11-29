import pandas as pd
from .area_lookup import AREA_AVG_PRICE

INPUT_COLUMNS = [
  "Bedrooms",
  "Bathrooms",
  "Size",
  "Area_Avg_Price",
  "Property Type",
  "Area",
  "Postcode"
]

def prepare_input(raw: dict) -> pd.DataFrame:

  # numeric
  bedrooms = float(raw["Bedrooms"])
  bathrooms = float(raw["Bathrooms"])
  size = float(raw["Size"])

  # categorical (use raw keys EXACTLY as they appear in HTML)
  property_type = raw["Property Type"].strip()
  area = raw["Area"].strip()
  postcode = raw["Postcode"].strip().upper()

  # Auto-fill average price
  area_avg_price = AREA_AVG_PRICE.get(area)

  if area_avg_price is None:
    raise ValueError(f"Unknown area '{area}'. Cannot compute Area_Avg_Price.")

  df = pd.DataFrame([{
    "Bedrooms": bedrooms,
    "Bathrooms": bathrooms,
    "Size": size,
    "Area_Avg_Price": area_avg_price,
    "Property Type": property_type,
    "Area": area,
    "Postcode": postcode
  }])

  return df[INPUT_COLUMNS]
