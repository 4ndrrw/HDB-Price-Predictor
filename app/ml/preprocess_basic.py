# app/ml/preprocess_basic.py

import pandas as pd

def prepare_basic_input(form_dict):
    """
    Prepare input for BASIC pipeline model.
    Unified field:
        area = town (basic mode)
    """

    area = (form_dict.get("town") or "").strip()   # merged area field

    data = {
        "area": [area],                                # <--- unified location field
        "flat_type": [(form_dict.get("flat_type") or "").strip()],
        "floor_area_sqm": [float(form_dict.get("floor_area_sqm") or 0)],
        "remaining_lease": [float(form_dict.get("remaining_lease") or 0)],
    }

    return pd.DataFrame(data)
