# app/ml/preprocess_precise.py

import pandas as pd
from app.ml.address_lookup import get_lat_lon

def prepare_precise_input(form_dict):

    town = (form_dict.get("town") or "").strip()
    street_name = (form_dict.get("street_name") or "").strip()
    storey_range = (form_dict.get("storey_range") or "").strip()
    flat_type = (form_dict.get("flat_type") or "").strip()
    flat_model = (form_dict.get("flat_model") or "").strip()
    address = (form_dict.get("address") or "").strip()

    # numbers
    floor_area = float(form_dict.get("floor_area_sqm") or 0)
    remaining_lease = float(form_dict.get("remaining_lease") or 0)

    # REAL lat/lon lookup from dataset
    lat, lon = get_lat_lon(address)

    if lat is None:
        lat = 0.0
    if lon is None:
        lon = 0.0

    data = {
        "town": [town],
        "street_name": [street_name],
        "storey_range": [storey_range],
        "flat_type": [flat_type],
        "flat_model": [flat_model],
        "floor_area_sqm": [floor_area],
        "remaining_lease": [remaining_lease],
        "latitude": [lat],
        "longitude": [lon]
    }

    return pd.DataFrame(data)
