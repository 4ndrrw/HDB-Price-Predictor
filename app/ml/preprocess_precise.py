# app/ml/preprocess_precise.py

import pandas as pd
from app.ml.address_lookup import get_address_details

def prepare_precise_input(form):
    """
    Prepare input for the precise model.
    If OneMap cannot validate the address, return (None, "invalid").
    """

    address = form["address"].strip()

    storey_range = form.get("storey_range")
    flat_type = form.get("flat_type")
    floor_area = float(form.get("floor_area_sqm") or 0)
    remaining_lease = float(form.get("remaining_lease") or 0)

    # -----------------------------
    # OneMap Lookup
    # -----------------------------
    details = get_address_details(address)

    # INVALID ADDRESS → STOP EVERYTHING
    if not details:
        return None, "invalid"   # <-- router must handle this

    # -----------------------------
    # VALID OneMap result
    # -----------------------------
    road_name = details["road_name"].upper().strip()  # match training format
    latitude = details["latitude"]
    longitude = details["longitude"]

    # MODEL INPUT
    X = pd.DataFrame([{
        "location": road_name,          # model feature
        "storey_range": storey_range,
        "flat_type": flat_type,
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease,
        "latitude": latitude,
        "longitude": longitude,
    }])

    # DB METADATA
    meta = {
        "location": address,      # full user-entered address
        "address": address,
        "storey_range": storey_range,
        "flat_type": flat_type,
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease,
        "latitude": latitude,
        "longitude": longitude,
    }

    return X, meta
