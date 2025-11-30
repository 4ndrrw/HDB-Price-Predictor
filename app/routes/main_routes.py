from flask import Blueprint, redirect, render_template, request, session
from joblib import load

from app.ml.preprocess import prepare_input
from app.models.prediction import PredictionHistory
from app.database import get_db

main_bp = Blueprint("main", __name__)

# Load ML model once
model = load("app/ml/model.pkl")


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

    user_id = session.get("user_id")      # <-- Logged-in user?
    user_logged_in = user_id is not None  # <-- Boolean flag for template logic

    # -----------------------------
    # POST → generate prediction
    # -----------------------------
    if request.method == "POST":
        form = request.form.to_dict()
        X = prepare_input(form)
        result = model.predict(X)[0]

        # Save ONLY if logged in
        PredictionHistory.save(form, result)

        # PRG redirect
        return redirect(f"/predict?temp_result={result}")

    # -----------------------------
    # GET → show form + optional result + history
    # -----------------------------
    temp_result = request.args.get("temp_result")

    # Load only this user's records
    if user_logged_in:
        records = PredictionHistory.get_all(user_id)
    else:
        records = None   # logged out → no history

    return render_template(
        "predict.html",
        result=temp_result,
        records=records,
        user_logged_in=user_logged_in
    )


# -----------------------------
# Clear History (Per-user)
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


# -----------------------------
# Test Page
# -----------------------------
@main_bp.route("/test")
def test_page():
    return open("app/test.html").read()
