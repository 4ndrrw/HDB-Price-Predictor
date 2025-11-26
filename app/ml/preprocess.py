import pandas as pd
import joblib

# -----------------------
# Load target encoding maps
# -----------------------
postcode_te_map = joblib.load("app/ml/postcode_te_map.pkl")
postcode_sector_te_map = joblib.load("app/ml/postcode_sector_te_map.pkl")
area_te_map = joblib.load("app/ml/area_te_map.pkl")

# -----------------------
# Expected Feature Order
# -----------------------
INPUT_COLUMNS = [
  "Bedrooms", "Bathrooms", "Size", "Area_Avg_Price",
  "Postcode_TE", "Postcode_Sector_TE", "Area_TE",
  "Property Type", "Area", "Postcode_Sector"
]

# -----------------------
# Helper functions
# -----------------------

def extract_postcode_sector(postcode: str) -> str:
  """
  Extract the postcode sector (1 or 2 digits) from the postcode string.
  Example: SW1A 2AA -> 'SW1A'
  """
  postcode = postcode.strip().upper()
  return postcode.split()[0]  # typical UK format

def safe_map(value, mapping, default=0):
  """
  Maps a value using a dictionary; returns default if missing.
  """
  return mapping.get(value, default)

# -----------------------
# Main Preprocessing Function
# -----------------------

def prepare_input(raw):
  """
  raw: dict coming from Flask form.
  Returns a pandas DataFrame with the correct columns and values
  ready for model.predict().
  """

  # ---- Extract original user inputs ----
  bedrooms = float(raw["Bedrooms"])
  bathrooms = float(raw["Bathrooms"])
  size = float(raw["Size"])
  area_avg_price = float(raw["Area_Avg_Price"])
  property_type = raw["Property Type"].strip()
  area = raw["Area"].strip()
  postcode = raw["Postcode"].strip()

  # ---- Derived: Postcode Sector ----
  postcode_sector = extract_postcode_sector(postcode)

  # ---- Target Encodings ----
  postcode_te = safe_map(postcode, postcode_te_map)
  postcode_sector_te = safe_map(postcode_sector, postcode_sector_te_map)
  area_te = safe_map(area, area_te_map)

  # ---- Build DataFrame in exact order ----
  data = {
    "Bedrooms": [bedrooms],
    "Bathrooms": [bathrooms],
    "Size": [size],
    "Area_Avg_Price": [area_avg_price],
    "Postcode_TE": [postcode_te],
    "Postcode_Sector_TE": [postcode_sector_te],
    "Area_TE": [area_te],
    "Property Type": [property_type],
    "Area": [area],
    "Postcode_Sector": [postcode_sector]
  }

  df = pd.DataFrame(data)
  df = df[INPUT_COLUMNS]  # ensure strict ordering

  return df
