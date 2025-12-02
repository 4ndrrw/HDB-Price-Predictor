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

        # Which model? ("basic" or "precise")
        mode = form.get("mode", "precise")  # default = precise

        # Preprocess based on mode
        if mode == "basic":
            X = prepare_basic_input(form)
            result = basic_model.predict(X)[0]
        else:
            X = prepare_precise_input(form)
            result = precise_model.predict(X)[0]

        # Store mode so history can differentiate
        form["mode"] = mode

        # Save ONLY if logged in
        if user_logged_in:
            PredictionHistory.save(form, result)

        # PRG pattern
        return redirect(f"/predict?temp_result={result}&mode={mode}")

    # -----------------------------
    # GET → Show Form + Optional Result + History
    # -----------------------------
    temp_result = request.args.get("temp_result")
    active_mode = request.args.get("mode", "precise")

    # Load this user's records
    if user_logged_in:
        records = PredictionHistory.get_all(user_id)
    else:
        records = None

    return render_template(
        "predict.html",
        result=temp_result,
        records=records,
        user_logged_in=user_logged_in,
        active_mode=active_mode
    )


# -----------------------------
# Clear History (per-user)
# -----------------------------
@main_bp.route("/clear_history")
def clear_history():

    user_id = session.get("user_id")

    # Must be logged in
    if not user_id:
        return redirect("/login")

    db = get_db()
    db.execute("DELETE FROM predictions WHERE user_id = ?", (user_id,))
    db.commit()

    return redirect("/predict")
