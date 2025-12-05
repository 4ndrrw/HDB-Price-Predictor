from flask import Blueprint, redirect, render_template, request, session
import joblib, json

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

    # =============================================================
    # POST → Generate Prediction
    # =============================================================
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

            area = float(form.get("floor_area_sqm"))
            lease = float(form.get("remaining_lease"))

            if not (30 <= area <= 200):
                return redirect("/predict?error=invalid_area&mode=basic")
            if not (55 <= lease <= 99):
                return redirect("/predict?error=invalid_lease&mode=basic")

            # Prepare model input
            X, meta = prepare_basic_input(form)
            result = basic_model.predict(X)[0]
            ppsqm = result / area

            # -----------------------------
            # Generate Dynamic Insights
            # -----------------------------
            insights = generate_insights(
                ppsqm=ppsqm,
                flat_type=form.get("flat_type"),
                storey=None,
                area=area,
                lease=lease,
                town=form.get("town"),
            )

            # Save history
            if user_logged_in:
                meta["mode"] = "basic"
                meta["price_per_sqm"] = ppsqm
                PredictionHistory.save(meta, result)

            # Redirect with insights
            return redirect(
                f"/predict?temp_result={result}&ppsqm={ppsqm}"
                f"&mode=basic&insights={json.dumps(insights)}"
            )

        # =====================================================
        # PRECISE MODE
        # =====================================================
        elif mode == "precise":
            required = ["storey_range", "flat_type", "floor_area_sqm",
                        "remaining_lease", "address"]

            if any(is_empty(f) for f in required):
                return redirect("/predict?error=missing_precise&mode=precise")

            area = float(form.get("floor_area_sqm"))
            lease = float(form.get("remaining_lease"))

            if not (30 <= area <= 200):
                return redirect("/predict?error=invalid_area&mode=precise")
            if not (55 <= lease <= 99):
                return redirect("/predict?error=invalid_lease&mode=precise")

            X, meta = prepare_precise_input(form)

            if X is None and meta == "invalid":
                return redirect("/predict?error=invalid_address&mode=precise")

            result = precise_model.predict(X)[0]
            ppsqm = result / area

            # -----------------------------
            # Generate Dynamic Insights
            # -----------------------------
            insights = generate_insights(
                ppsqm=ppsqm,
                flat_type=form.get("flat_type"),
                storey=form.get("storey_range"),
                area=area,
                lease=lease,
                town=meta.get("location"),
            )

            if user_logged_in:
                meta["mode"] = "precise"
                meta["price_per_sqm"] = ppsqm
                PredictionHistory.save(meta, result)

            return redirect(
                f"/predict?temp_result={result}&ppsqm={ppsqm}"
                f"&mode=precise&insights={json.dumps(insights)}"
            )

    # =============================================================
    # GET → Render Page
    # =============================================================
    raw_insights = request.args.get("insights")
    insights = json.loads(raw_insights) if raw_insights else []

    temp_result = request.args.get("temp_result")
    active_mode = request.args.get("mode", "precise")
    records = PredictionHistory.get_all(user_id) if user_logged_in else None

    return render_template(
        "predict.html",
        result=temp_result,
        ppsqm=request.args.get("ppsqm"),
        insights=insights,
        records=records,
        user_logged_in=user_logged_in,
        active_mode=active_mode,
    )


# =============================================================
# CLEAR HISTORY
# =============================================================
@main_bp.route("/clear_history")
def clear_history():

    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    db = get_db()
    db.execute("DELETE FROM predictions WHERE user_id = ?", (user_id,))
    db.commit()

    return redirect("/predict")


# =============================================================
# DYNAMIC INSIGHT GENERATOR
# =============================================================
def generate_insights(ppsqm, flat_type, storey, area, lease, town):
    insights = []

    # Market PPSQM
    if ppsqm > 6000:
        insights.append("Price per sqm is above typical resale levels, indicating strong demand in this area.")
    elif ppsqm < 4500:
        insights.append("Valuation is below market average, suggesting potential value-for-money conditions.")
    else:
        insights.append("Price per sqm aligns with typical resale market ranges.")

    # Flat type behaviour
    if "4 ROOM" in flat_type:
        insights.append("4-room flats maintain stable demand across most towns.")
    elif "3 ROOM" in flat_type:
        insights.append("3-room flats appeal mainly to budget-conscious buyers, affecting price sensitivity.")
    elif "5 ROOM" in flat_type:
        insights.append("5-room flats often see wider price variation due to differing buyer demographics.")

    # Storey range insights
    if storey:
        if storey in ["01 TO 03", "04 TO 06"]:
            insights.append("Lower-floor units tend to transact slightly lower due to noise and limited views.")
        elif storey in ["07 TO 09", "10 TO 12", "13 TO 15"]:
            insights.append("Mid-floor units often command balanced valuations.")
        else:
            insights.append("High-floor units typically enjoy premiums from views and ventilation.")

    # Unit size dynamics
    if area > 110:
        insights.append("Larger units attract multi-generational buyers, increasing competitive pressure.")
    elif area < 70:
        insights.append("Compact units often produce higher rental yield potential.")
    else:
        insights.append("Mid-sized units tend to maintain strong resale demand.")

    return insights[:3]  # ensure exactly 3 insights
