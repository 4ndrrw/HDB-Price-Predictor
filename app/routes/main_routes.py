from flask import Blueprint, render_template, request
from joblib import load
from app.ml.preprocess import prepare_input
from app.models.prediction import PredictionHistory

main_bp = Blueprint("main", __name__)

model = load("app/ml/model.pkl")

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/predict", methods=["POST"])
def predict():
    form = request.form.to_dict()
    X = prepare_input(form)

    prediction = model.predict(X)[0]

    # Save history
    PredictionHistory.save(form, prediction)

    # TEMPORARY — avoids template error
    return f"Predicted price: {prediction}"

@main_bp.route("/test")
def test_page():
    return open("app/test.html").read()