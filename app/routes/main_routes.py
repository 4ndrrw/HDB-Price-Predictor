from flask import Blueprint, render_template, request
from joblib import load

from app.ml.preprocess import prepare_input
from app.models.prediction import PredictionHistory

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

    result = None  # prediction output

    # If POST → run model, save prediction
    if request.method == "POST":
        form = request.form.to_dict()
        X = prepare_input(form)
        result = model.predict(X)[0]

        # Save into database
        PredictionHistory.save(form, result)

    # Always load history for table
    records = PredictionHistory.get_all()

    # Render the combined predict + history page
    return render_template("predict.html", result=result, records=records)


# -----------------------------
# Test Page 
# -----------------------------
@main_bp.route("/test")
def test_page():
    return open("app/test.html").read()
