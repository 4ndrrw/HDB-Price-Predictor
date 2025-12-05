import pandas as pd
from app.ml.address_lookup import get_address_details

def prepare_precise_input(form):
    """
    Build final row for the precise model AND metadata for DB.
    Uses live OneMap API lookup.
    """

    # 1. User Inputs
    raw_address = form["address"]
    address = raw_address.strip()

    storey_range = form["storey_range"]
    flat_type = form["flat_type"]

    floor_area = float(form.get("floor_area_sqm", 100) or 100)
    remaining_lease = float(form.get("remaining_lease", 70) or 70)

    # 2. OneMap Lookup
    details = get_address_details(address)

    if details:
        area = details["road_name"]              # <-- merged field
        latitude = details["latitude"]
        longitude = details["longitude"]
    else:
        area = "UNKNOWN"
        latitude = 0.0
        longitude = 0.0

    # 3. Build model input row
    X = pd.DataFrame([{
        "area": area,                           # <-- model now uses unified area field
        "storey_range": storey_range,
        "flat_type": flat_type,
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease,
        "latitude": latitude,
        "longitude": longitude,
    }])

    # 4. Metadata for saving into DB
    meta = {
        "area": area,
        "address": address,
        "storey_range": storey_range,
        "flat_type": flat_type,
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease,
        "latitude": latitude,
        "longitude": longitude,
    }

    return X, meta
