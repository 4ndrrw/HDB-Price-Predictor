import pandas as pd

# Load the geocoded lookup table once when module loads
addr_df = pd.read_csv("app/ml/data/Flat prices geocoded.csv")
addr_df["address_clean"] = addr_df["address"].str.strip().str.upper()

addr_lookup = (
    addr_df[["address_clean", "town", "street_name", "latitude", "longitude"]]
    .drop_duplicates("address_clean")
    .set_index("address_clean")
)


def prepare_precise_input(form):
    """
    Build final row for the precise model AND metadata for DB.

    User inputs:
        - address
        - storey_range
        - flat_type
        - floor_area_sqm
        - remaining_lease

    Derived from lookup:
        - town
        - street_name
        - latitude
        - longitude
    """

    # 1. Extract user inputs
    address = form["address"].strip().upper()
    storey_range = form["storey_range"]
    flat_type = form["flat_type"]

    # Defaults prevent NaNs entering model
    floor_area = float(form.get("floor_area_sqm", 100) or 100)
    remaining_lease = float(form.get("remaining_lease", 70) or 70)

    # 2. Lookup metadata
    if address in addr_lookup.index:
        row = addr_lookup.loc[address]
        town = row["town"]
        street_name = row["street_name"]
        latitude = float(row["latitude"])
        longitude = float(row["longitude"])
    else:
        # Fallback to avoid NaN in pipeline
        town = "UNKNOWN"
        street_name = "UNKNOWN"
        latitude = 0.0
        longitude = 0.0

    # 3. Build model input DataFrame
    X = pd.DataFrame([{
        "town": town,
        "street_name": street_name,
        "storey_range": storey_range,
        "flat_type": flat_type,
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease,
        "latitude": latitude,
        "longitude": longitude,
    }])

    # 4. Build metadata dict for saving into DB
    meta = {
        "town": town,
        "street_name": street_name,
        "storey_range": storey_range,
        "flat_type": flat_type,
        "floor_area_sqm": floor_area,
        "remaining_lease": remaining_lease,
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
    }

    return X, meta
