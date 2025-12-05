import requests

BASE_URL = "https://www.onemap.gov.sg/api/common/elastic/search"

def get_address_details(address: str):
    """Query OneMap for address search & geocoding."""
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

        # No results
        if not data.get("results"):
            return None

        result = data["results"][0]

        return {
            "latitude": float(result["LATITUDE"]),
            "longitude": float(result["LONGITUDE"]),
            "building": result.get("BUILDING", ""),
            "block": result.get("BLK_NO", ""),
            "road_name": result.get("ROAD_NAME", ""),
            "postal_code": result.get("POSTAL", ""),
            "full_address": result.get("ADDRESS", "")
        }

    except Exception as e:
        print("OneMap API error:", e)
        return None
