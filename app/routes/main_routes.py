from flask import Blueprint, redirect, render_template, request
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
  return render_template("home.html")   # updated from index.html


# -----------------------------
# Predict Page (GET + POST)
# -----------------------------
@main_bp.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "POST":
        form = request.form.to_dict()
        X = prepare_input(form)
        result = model.predict(X)[0]

        PredictionHistory.save(form, result)

        # Redirect with temp params
        return redirect(f"/predict?temp_result={result}")

    # GET handling
    temp_result = request.args.get("temp_result")

    records = PredictionHistory.get_all()

    if temp_result:
        # Render once WITH result
        response = render_template("predict.html", result=temp_result, records=records)

        # After rendering, immediately clean URL via JS
        return response

    # No result → clean state
    return render_template("predict.html", result=None, records=records)

# -----------------------------
# Test Page 
# -----------------------------
@main_bp.route("/test")
def test_page():
  return open("app/test.html").read()
