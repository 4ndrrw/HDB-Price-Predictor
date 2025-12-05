def validate_inputs(data):
    required = ["area", "rooms"]

    for r in required:
        if r not in data:
            raise KeyError(f"Missing field: {r}")

    if not isinstance(data["area"], (int, float)):
        raise TypeError("Area must be numeric")

    if not isinstance(data["rooms"], int):
        raise TypeError("Rooms must be an integer")

    # NEW RULE → does NOT allow negative or zero rooms
    if data["rooms"] <= 0:
        raise TypeError("Rooms must be a positive integer")

    return True


def check_range(key, value):
    rules = {
        "area": (0, 5000),
        "rooms": (1, 10)
    }

    min_v, max_v = rules[key]
    return min_v <= value <= max_v


def ensure_consistency(data):
    # basic logical rule: price must scale with area
    return (data["price"] / data["area"]) > 1000
