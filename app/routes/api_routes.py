from flask import Blueprint, request, jsonify, session
import joblib
from app.ml.preprocess_basic import prepare_basic_input
from app.ml.preprocess_precise import prepare_precise_input
from app.models.prediction import PredictionHistory

api_bp = Blueprint("api", __name__)

# Load HDB models
basic_model = joblib.load("app/ml/rf_model_basic.pkl")
precise_model = joblib.load("app/ml/rf_model_precise.pkl")


@api_bp.route("/predict", methods=["POST"])
def api_predict():
    data = request.json or {}
    mode = data.get("mode", "precise")

    # Validate required fields
    if mode == "basic":
        required = ["town", "flat_type", "floor_area_sqm", "remaining_lease"]
    else:
        required = ["storey_range", "flat_type", "floor_area_sqm", "remaining_lease", "address"]

    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Choose model + preprocessing (CORRECTED unpack)
    if mode == "basic":
        X, meta = prepare_basic_input(data)
        model = basic_model
    else:
        X, meta = prepare_precise_input(data)
        model = precise_model

    # Predict
    prediction = float(model.predict(X)[0])

    # Save prediction history (if logged in)
    user_id = session.get("user_id")
    if user_id:
        PredictionHistory.save(data, prediction)

    return jsonify({"prediction": prediction, "mode": mode}), 200


@api_bp.route("/history")
def api_history():
    """
    Return logged-in user's prediction history as JSON.
    If not logged in → empty list.
    """

    user_id = session.get("user_id")
    rows = PredictionHistory.get_all(user_id)

    return jsonify(rows)
