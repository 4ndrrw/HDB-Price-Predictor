import pandas as pd

# Load geocoded CSV once globally
df = pd.read_csv("app/ml/data/Flat prices geocoded.csv")

# Build fast dictionary lookup
ADDRESS_TO_LAT = dict(zip(df["address"].str.upper(), df["latitude"]))
ADDRESS_TO_LON = dict(zip(df["address"].str.upper(), df["longitude"]))

def get_lat_lon(address: str):
    if not address:
        return None, None

    key = address.upper().strip()
    lat = ADDRESS_TO_LAT.get(key)
    lon = ADDRESS_TO_LON.get(key)

    return lat, lon
