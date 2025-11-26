import pandas as pd

# Expected raw input columns (Flask should send these keys)
INPUT_COLUMNS = [
    "Bedrooms", "Bathrooms", "Size", "Area_Avg_Price",
    "Property Type", "Area", "Postcode"
]

def extract_str(v):
    return "" if v is None else str(v).strip()

def prepare_input(raw: dict) -> pd.DataFrame:
    """
    Accepts raw form/json dict from Flask and returns DataFrame with raw columns.
    The saved pipeline (model.pkl) will perform target-encoding and preprocessing.
    """
    bedrooms = float(raw.get("Bedrooms", 0))
    bathrooms = float(raw.get("Bathrooms", 0))
    size = float(raw.get("Size", 0))
    area_avg_price = float(raw.get("Area_Avg_Price", 0))

    property_type = extract_str(raw.get("Property Type"))
    area = extract_str(raw.get("Area"))
    postcode = extract_str(raw.get("Postcode")).upper()

    data = {
        "Bedrooms": [bedrooms],
        "Bathrooms": [bathrooms],
        "Size": [size],
        "Area_Avg_Price": [area_avg_price],
        "Property Type": [property_type],
        "Area": [area],
        "Postcode": [postcode],
    }

    df = pd.DataFrame(data)
    # ensure columns exist in expected order
    df = df.reindex(columns=INPUT_COLUMNS)
    return df