# app/ml/preprocess_precise.py

import pandas as pd
from typing import Tuple, Optional


def geocode_address(address: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Placeholder geocoding helper.

    Currently returns (None, None).
    You can replace this with a real geocoding call (e.g. OneMap API)
    so that latitude/longitude are populated based on the 'address' field.

    For now, the model pipeline should be robust to missing lat/lon
    (or you can choose to drop those features in training).
    """
    address = (address or "").strip()
    if not address:
        return None, None

    # TODO: Plug in your actual geocoding function here.
    # Example (pseudo):
    # lat, lon = get_lat_lon_from_onemap(address)
    # return lat, lon

    return None, None


def prepare_precise_input(form_dict):
    """
    Prepare input for the PRECISE model.

    Expected form fields (from predict.html):
      - town
      - street_name
      - storey_range
      - flat_type
      - flat_model
      - floor_area_sqm
      - remaining_lease
      - address   (used for lat/lon if you wire up geocoding)

    Returns:
      A pandas DataFrame with a single row, with column names matching
      what the precise model pipeline was trained on.
    """

    town = (form_dict.get("town") or "").strip()
    street_name = (form_dict.get("street_name") or "").strip()
    storey_range = (form_dict.get("storey_range") or "").strip()
    flat_type = (form_dict.get("flat_type") or "").strip()
    flat_model = (form_dict.get("flat_model") or "").strip()
    address = (form_dict.get("address") or "").strip()

    # numeric fields
    try:
        floor_area = float(form_dict.get("floor_area_sqm") or 0)
    except ValueError:
        floor_area = 0.0

    try:
        remaining_lease = float(form_dict.get("remaining_lease") or 0)
    except ValueError:
        remaining_lease = 0.0

    # Optional: geocode address → lat/lon
    latitude, longitude = geocode_address(address)

    data = {
        "town": [town],
        "street_name": [street_name],
        "storey_range": [storey_range],
        "flat_type": [flat_type],
        "flat_model": [flat_model],
        "floor_area_sqm": [floor_area],
        "remaining_lease": [remaining_lease],
        "address": [address],
        # If your precise model uses these, keep them;
        # if not, you can drop these columns in training.
        "latitude": [latitude],
        "longitude": [longitude],
    }

    return pd.DataFrame(data)
