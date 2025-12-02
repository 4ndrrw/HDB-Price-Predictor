# app/ml/preprocess_basic.py

import pandas as pd

def prepare_basic_input(form_dict):
    """
    Prepare input for BASIC pipeline model.
    Pipeline handles all encoding internally.
    """

    data = {
        "town": [ (form_dict.get("town") or "").strip() ],
        "flat_type": [ (form_dict.get("flat_type") or "").strip() ],
        "floor_area_sqm": [ float(form_dict.get("floor_area_sqm") or 0) ],
        "remaining_lease": [ float(form_dict.get("remaining_lease") or 0) ]
    }

    return pd.DataFrame(data)
