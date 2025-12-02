# app/ml/preprocess_basic.py

import pandas as pd


def prepare_basic_input(form_dict):
    """
    Prepare input for the BASIC (quick estimate) model.

    Expected form fields (from predict.html):
      - town
      - flat_type
      - floor_area_sqm
      - remaining_lease

    Returns:
      A pandas DataFrame with a single row, with column names matching
      what the basic model pipeline was trained on.
    """

    town = (form_dict.get("town") or "").strip()
    flat_type = (form_dict.get("flat_type") or "").strip()

    # numeric fields: be defensive
    try:
        floor_area = float(form_dict.get("floor_area_sqm") or 0)
    except ValueError:
        floor_area = 0.0

    try:
        remaining_lease = float(form_dict.get("remaining_lease") or 0)
    except ValueError:
        remaining_lease = 0.0

    data = {
        "town": [town],
        "flat_type": [flat_type],
        "floor_area_sqm": [floor_area],
        "remaining_lease": [remaining_lease],
    }

    # Single-row DataFrame, ready for model.predict
    return pd.DataFrame(data)
