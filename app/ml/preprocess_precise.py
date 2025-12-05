# app/ml/preprocess_precise.py

import pandas as pd
from app.ml.address_lookup import get_address_details

def prepare_precise_input(form):

    address = form["address"].strip()

    storey_range = form["storey_range"]
    flat_type = form["flat_type"]
    floor_area = float(form.get("floor_area_sqm", 100) or 100)
    remaining_lease = float(form.get("remaining_lease", 70) or 70)

    details = get_address_details(address)

    if details:
        location = details["road_name"]   # model feature
        latitude = details["latitude"]
        longitude = details["longitude"]
    else:
        location = "UNKNOWN"
        latitude = longitude = 0.0

    # MODEL INPUT
    X = pd.DataFrame([{
        "location": location,
        "storey_range": storey_range,
        "flat_type": flat_type,
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease,
        "latitude": latitude,
        "longitude": longitude,
    }])

    # DB METADATA
    meta = {
        "location": address,     # full address stored for history
        "address": address,
        "storey_range": storey_range,
        "flat_type": flat_type,
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease,
        "latitude": latitude,
        "longitude": longitude,
    }

    return X, meta
