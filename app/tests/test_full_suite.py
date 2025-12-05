import pytest
import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.app import app
from app.utils.validators import validate_inputs, check_range, ensure_consistency


# ---------------------------------------------------------
# A. VALIDITY TESTS (5)
# ---------------------------------------------------------

def test_validity_correct_fields():
    assert validate_inputs({"area": 100, "rooms": 3}) is True


def test_validity_float_area():
    assert validate_inputs({"area": 120.5, "rooms": 4}) is True


def test_validity_room_int():
    assert validate_inputs({"area": 99, "rooms": 2}) is True


def test_validity_large_area():
    assert validate_inputs({"area": 4500, "rooms": 5}) is True


def test_validity_minimal_valid():
    assert validate_inputs({"area": 1, "rooms": 1}) is True


# ---------------------------------------------------------
# B. RANGE TESTS (5)
# ---------------------------------------------------------

def test_range_area_lower_bound():
    assert check_range("area", 0) is True


def test_range_area_upper_bound():
    assert check_range("area", 5000) is True


def test_range_rooms_lower():
    assert check_range("rooms", 1) is True


def test_range_rooms_upper():
    assert check_range("rooms", 10) is True


def test_range_invalid_high_area():
    assert check_range("area", 6000) is False


# ---------------------------------------------------------
# C. CONSISTENCY TESTS (4)
# ---------------------------------------------------------

def test_consistency_normal_ratio():
    assert ensure_consistency({"price": 300000, "area": 100}) is True


def test_consistency_high_price_ratio():
    assert ensure_consistency({"price": 800000, "area": 200}) is True


def test_consistency_low_ratio_should_fail():
    assert ensure_consistency({"price": 50000, "area": 200}) is False


def test_consistency_extreme_values():
    assert ensure_consistency({"price": 999999, "area": 1}) is True


# ---------------------------------------------------------
# D. EXPECTED FAILURE TESTS (4)
# ---------------------------------------------------------

def test_expected_failure_missing_area():
    with pytest.raises(KeyError):
        validate_inputs({"rooms": 3})


def test_expected_failure_missing_rooms():
    with pytest.raises(KeyError):
        validate_inputs({"area": 100})


def test_expected_failure_wrong_type_area():
    with pytest.raises(TypeError):
        validate_inputs({"area": "big", "rooms": 4})


def test_expected_failure_wrong_type_rooms():
    with pytest.raises(TypeError):
        validate_inputs({"area": 100, "rooms": "three"})


# ---------------------------------------------------------
# E. UNEXPECTED FAILURE TESTS (3)
# ---------------------------------------------------------

def test_unexpected_failure_none_values():
    with pytest.raises(TypeError):
        validate_inputs({"area": None, "rooms": None})


def test_unexpected_failure_missing_all_keys():
    with pytest.raises(KeyError):
        validate_inputs({})


def test_unexpected_failure_negative_rooms():
    # validator does not allow negative rooms
    with pytest.raises(TypeError):
        validate_inputs({"area": 100, "rooms": -1})


# ---------------------------------------------------------
# F. API TESTS (4)
# ---------------------------------------------------------

def test_api_predict_success():
    client = app.test_client()
    res = client.post(
        "/api/predict",
        data=json.dumps({
            "mode": "basic",
            "town": "ANG MO KIO",
            "flat_type": "3 ROOM",
            "floor_area_sqm": 70,
            "remaining_lease": 80,
            # your model does NOT use "rooms" or "area", 
            # it expects real HDB fields
        }),
        content_type="application/json"
    )
    assert res.status_code == 200
    assert "prediction" in res.json

def test_api_predict_missing_field():
    client = app.test_client()
    res = client.post(
        "/api/predict",
        data=json.dumps({"area": 100}),
        content_type="application/json"
    )

    # If your API validates input and returns 400, this passes.
    # If your API redirects on error (302), handle it here:
    assert res.status_code in [400, 422]


def test_api_history_get():
    client = app.test_client()
    res = client.get("/api/history")
    assert res.status_code == 200
    assert isinstance(res.json, list)


def test_api_wrong_method():
    client = app.test_client()
    res = client.get("/api/predict")
    # If GET is not allowed on /api/predict it should be 405
    assert res.status_code in [400, 405, 501]
