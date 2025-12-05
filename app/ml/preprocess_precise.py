# app/ml/preprocess_precise.py

import pandas as pd
from app.ml.address_lookup import get_address_details

def prepare_precise_input(form):
    """
    Prepare input for the precise model.
    If OneMap cannot validate the address, return (None, "invalid").
    """

    # -------------------------
    # Extract Raw Form Inputs
    # -------------------------
    raw_address = form["address"].strip()

    raw_flat_type = (form.get("flat_type") or "").strip()
    raw_storey_raw = form.get("storey_range")        # e.g. "07 TO 09"
    raw_storey_label = form.get("storey_label")      # e.g. "06–10"

    floor_area = float(form.get("floor_area_sqm") or 0)
    remaining_lease = float(form.get("remaining_lease") or 0)

    # ----------------------------------------------------
    # OneMap Lookup
    # ----------------------------------------------------
    details = get_address_details(raw_address)

    if not details:
        return None, "invalid"

    # -------------------------
    # Prepare location strings
    # -------------------------
    model_location = details["road_name"].upper().strip()   # model format
    
    block = details.get("block", "").strip()
    road = details.get("road_name", "").title().strip()

    # e.g. "406 Ang Mo Kio Ave 10"
    db_location = f"{block} {road}".strip()

    latitude = details["latitude"]
    longitude = details["longitude"]

    # ----------------------------------------------------
    # MODEL INPUT (uppercase & numeric)
    # ----------------------------------------------------
    X = pd.DataFrame([{
        "location": model_location,
        "storey_range": raw_storey_raw,           # RAW for model ("07 TO 09")
        "flat_type": raw_flat_type.upper(),       # model expects uppercase
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease,
        "latitude": latitude,
        "longitude": longitude,
    }])

    # ----------------------------------------------------
    # DB METADATA (clean, nice for UI)
    # ----------------------------------------------------
    meta = {
        "location": db_location,                  # title case
        "address": raw_address,
        "storey_range": raw_storey_label,         # store pretty label e.g. "06–10"
        "flat_type": raw_flat_type.title(),       # display format
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease,
        "latitude": latitude,
        "longitude": longitude,
    }

    return X, meta
