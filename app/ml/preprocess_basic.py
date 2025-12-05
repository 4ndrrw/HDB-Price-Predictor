# app/ml/preprocess_basic.py

import pandas as pd

def prepare_basic_input(form_dict):

    location = (form_dict.get("town") or "").strip()

    X = pd.DataFrame([{
        "location": location,
        "flat_type": (form_dict.get("flat_type") or "").strip(),
        "floor_area_sqm": float(form_dict.get("floor_area_sqm") or 0),
        "remaining_lease": float(form_dict.get("remaining_lease") or 0),
    }])

    meta = {
        "location": location,
        "flat_type": form_dict.get("flat_type"),
        "floor_area_sqm": form_dict.get("floor_area_sqm"),
        "remaining_lease": form_dict.get("remaining_lease"),
    }

    return X, meta
