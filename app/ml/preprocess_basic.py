# app/ml/preprocess_basic.py

import pandas as pd

def prepare_basic_input(form):
    location = (form.get("town") or "").strip()
    flat_type = (form.get("flat_type") or "").strip()

    floor_area = float(form.get("floor_area_sqm") or 0)
    remaining_lease = float(form.get("remaining_lease") or 0)

    # Model input
    X = pd.DataFrame([{
        "location": location,
        "flat_type": flat_type,
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease
    }])

    # DB metadata
    meta = {
        "location": location,
        "flat_type": flat_type,
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease,
        "storey_range": None,
        "address": None,
        "latitude": None,
        "longitude": None,
    }

    return X, meta
