import requests

BASE_URL = "https://developers.onemap.sg/commonapi/search"

def get_address_details(address: str):
    """
    Calls OneMap API to retrieve latitude, longitude, block, road name, building, postal code, etc.
    Returns a dictionary with extracted fields or None if failed.
    """
    if not address:
        return None

    params = {
        "searchVal": address,
        "returnGeom": "Y",
        "getAddrDetails": "Y",
        "pageNum": 1
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        # If no results found → return None
        if data.get("found") == 0:
            return None

        result = data["results"][0]  # Take first match

        return {
            "latitude": float(result["LATITUDE"]),
            "longitude": float(result["LONGITUDE"]),
            "building": result.get("BUILDING", ""),
            "block": result.get("BLOCK", ""),
            "road_name": result.get("ROAD_NAME", ""),
            "postal_code": result.get("POSTAL", ""),
            "full_address": result.get("ADDRESS", "")
        }

    except requests.RequestException as e:
        print("OneMap API error:", e)
        return None
