import pandas as pd

# --------------------------------------------------------------------
# Columns your trained pipeline expects BEFORE any transformations
# --------------------------------------------------------------------
INPUT_COLUMNS = [
    "Bedrooms",
    "Bathrooms",
    "Size",
    "Area_Avg_Price",
    "Property Type",
    "Area",
    "Postcode"
]

def prepare_input(raw: dict) -> pd.DataFrame:
    """
    Prepares raw form input values for the ML pipeline.
    The returned DataFrame contains ONLY the 7 raw columns expected by
    the fitted Pipeline (TargetEncoder + ColumnTransformer + Model).

    No manual target encoding, scaling, or one-hot encoding is done here.
    The loaded model pipeline handles all transformations.
    """

    # Clean + convert fields
    try:
        bedrooms = float(raw["Bedrooms"])
        bathrooms = float(raw["Bathrooms"])
        size = float(raw["Size"])
        area_avg_price = float(raw["Area_Avg_Price"])
    except ValueError:
        raise ValueError("Numeric fields must be valid numbers.")

    property_type = str(raw["Property Type"]).strip()
    area = str(raw["Area"]).strip()
    postcode = str(raw["Postcode"]).strip().upper()

    # Construct a DataFrame in the EXACT required order
    df = pd.DataFrame([{
        "Bedrooms": bedrooms,
        "Bathrooms": bathrooms,
        "Size": size,
        "Area_Avg_Price": area_avg_price,
        "Property Type": property_type,
        "Area": area,
        "Postcode": postcode
    }])

    # Enforce strict column order to match training expectations
    return df[INPUT_COLUMNS]
