from flask import Blueprint, redirect, render_template, request, session
import joblib

from app.ml.preprocess_basic import prepare_basic_input
from app.ml.preprocess_precise import prepare_precise_input
from app.models.prediction import PredictionHistory
from app.database import get_db

main_bp = Blueprint("main", __name__)

# -----------------------------
# Load both models (HDB)
# -----------------------------
basic_model = joblib.load("app/ml/rf_model_basic.pkl")
precise_model = joblib.load("app/ml/rf_model_precise.pkl")


# -----------------------------
# Home Page
# -----------------------------
@main_bp.route("/")
def index():
    return render_template("home.html")


# -----------------------------
# Predict Page (GET + POST)
# -----------------------------
@main_bp.route("/predict", methods=["GET", "POST"])
def predict():

    user_id = session.get("user_id")
    user_logged_in = user_id is not None

    # -----------------------------
    # POST → Generate Prediction
    # -----------------------------
    if request.method == "POST":
        form = request.form.to_dict()
        mode = form.get("mode", "precise")

        def is_empty(name: str) -> bool:
            v = form.get(name)
            return v is None or str(v).strip() == ""

        # =====================================================
        # BASIC MODE
        # =====================================================
        if mode == "basic":
            required = ["town", "flat_type", "floor_area_sqm", "remaining_lease"]
            if any(is_empty(f) for f in required):
                return redirect("/predict?error=missing_basic&mode=basic")

            # ---- Validate ranges ----
            area = float(form.get("floor_area_sqm"))
            lease = float(form.get("remaining_lease"))

            if not (30 <= area <= 200):
                return redirect("/predict?error=invalid_area&mode=basic")

            if not (55 <= lease <= 99):
                return redirect("/predict?error=invalid_lease&mode=basic")

            # prepare_basic_input returns (X, meta)
            X, meta = prepare_basic_input(form)

            result = basic_model.predict(X)[0]

            if user_logged_in:
                meta["mode"] = "basic"
                PredictionHistory.save(meta, result)

        # =====================================================
        # PRECISE MODE
        # =====================================================
        elif mode == "precise":
            required = ["storey_range", "flat_type", "floor_area_sqm",
                        "remaining_lease", "address"]

            if any(is_empty(f) for f in required):
                return redirect("/predict?error=missing_precise&mode=precise")

            # ---- Validate ranges ----
            area = float(form.get("floor_area_sqm"))
            lease = float(form.get("remaining_lease"))

            if not (30 <= area <= 200):
                return redirect("/predict?error=invalid_area&mode=precise")

            if not (55 <= lease <= 99):
                return redirect("/predict?error=invalid_lease&mode=precise")

            # Prepare precise input
            X, meta = prepare_precise_input(form)

            # Invalid address caught via preprocess
            if X is None and meta == "invalid":
                return redirect("/predict?error=invalid_address&mode=precise")

            result = precise_model.predict(X)[0]

            if user_logged_in:
                meta["mode"] = "precise"
                PredictionHistory.save(meta, result)

    # -----------------------------
    # GET → render page
    # -----------------------------
    temp_result = request.args.get("temp_result")
    active_mode = request.args.get("mode", "precise")

    records = PredictionHistory.get_all(user_id) if user_logged_in else None

    return render_template(
        "predict.html",
        result=temp_result,
        records=records,
        user_logged_in=user_logged_in,
        active_mode=active_mode,
    )


# -----------------------------
# Clear History
# -----------------------------
@main_bp.route("/clear_history")
def clear_history():

    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    db = get_db()
    db.execute("DELETE FROM predictions WHERE user_id = ?", (user_id,))
    db.commit()

    return redirect("/predict")
