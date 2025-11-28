from flask import Blueprint, request, jsonify
from joblib import load
from app.ml.preprocess import prepare_input
from app.models.prediction import PredictionHistory

api_bp = Blueprint("api", __name__)

model = load("app/ml/model.pkl")

@api_bp.route("/predict", methods=["POST"])
def api_predict():
  data = request.json
  X = prepare_input(data)
  result = float(model.predict(X)[0])
  PredictionHistory.save(data, result)
  return jsonify({"prediction": result})

@api_bp.route("/history")
def api_history():
  rows = PredictionHistory.get_all()
  return jsonify([dict(row) for row in rows])
