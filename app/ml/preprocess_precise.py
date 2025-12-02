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
    Build final row for the precise model.
    Using ONLY these as user inputs:
    - address
    - storey_range
    - flat_type
    - floor_area_sqm
    - remaining_lease
    
    And automatically derive:
    - town
    - street_name
    - latitude
    - longitude
    """

    # 1. Extract from form
    address = form["address"].strip().upper()
    storey_range = form["storey_range"]
    flat_type = form["flat_type"]
    floor_area = float(form["floor_area_sqm"])
    remaining_lease = float(form["remaining_lease"])

    # 2. Lookup metadata (town, street_name, lat, lon)
    if address in addr_lookup.index:
        row = addr_lookup.loc[address]
        town = row["town"]
        street_name = row["street_name"]
        latitude = float(row["latitude"])
        longitude = float(row["longitude"])
    else:
        town = None
        street_name = None
        latitude = None
        longitude = None

    # 3. Build DataFrame for pipeline input
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

    return X
