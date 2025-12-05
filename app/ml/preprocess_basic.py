# app/ml/preprocess_basic.py

import pandas as pd

def prepare_basic_input(form):
    # Raw user input
    raw_location = (form.get("town") or "").strip()
    raw_flat_type = (form.get("flat_type") or "").strip()

    # Model needs UPPERCASE (matching training data)
    model_location = raw_location.upper()
    model_flat_type = raw_flat_type.upper()

    # UI/DB should show Title Case
    db_location = raw_location.title()
    db_flat_type = raw_flat_type.upper()  # Flat types usually stay uppercase (optional)
    # If you also want Flat Type in title case, uncomment:
    # db_flat_type = raw_flat_type.title()

    floor_area = float(form.get("floor_area_sqm") or 0)
    remaining_lease = float(form.get("remaining_lease") or 0)

    # Input sent to ML model
    X = pd.DataFrame([{
        "location": model_location,
        "flat_type": model_flat_type,
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease
    }])

    # Metadata saved into DB
    meta = {
        "location": db_location,      # ⬅ saved as Title Case
        "flat_type": db_flat_type,    # ⬅ UI-friendly
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease,
        "storey_range": None,
        "address": None,
        "latitude": None,
        "longitude": None,
    }

    return X, meta
