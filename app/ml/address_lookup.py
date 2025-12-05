import requests

BASE_URL = "https://developers.onemap.sg/commonapi/search"

def normalize(s: str) -> str:
    return s.replace(" ", "").lower()

def get_address_details(address: str):
    """
    Calls OneMap API to retrieve details, but rejects fuzzy matches.
    Address is considered VALID ONLY IF:
      - OneMap returns results
      - BLOCK + ROAD_NAME matches user's input (case-insensitive, space-insensitive)
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

        if data.get("found") == 0:
            return None

        result = data["results"][0]  # First match returned by OneMap

        block = result.get("BLOCK", "")
        road = result.get("ROAD_NAME", "")
        combined = f"{block} {road}".strip()

        # ----------------------------
        # STRICT VALIDATION
        # Reject if OneMap match does not appear in the input
        # ----------------------------
        if normalize(combined) not in normalize(address):
            return None  # Reject fuzzy match

        return {
            "latitude": float(result["LATITUDE"]),
            "longitude": float(result["LONGITUDE"]),
            "building": result.get("BUILDING", ""),
            "block": block,
            "road_name": road,
            "postal_code": result.get("POSTAL", ""),
            "full_address": result.get("ADDRESS", "")
        }

    except requests.RequestException as e:
        print("OneMap API error:", e)
        return None
