# Precision Property Analytics - HDB Resale Price Predictor

## Overview

Precision Property Analytics is a machine-learning-powered Flask web application designed to predict the resale prices of Singapore Housing & Development Board (HDB) flats. The application offers two intuitive valuation modes—**Basic** and **Precise**—tailored to different use cases. It leverages regression models trained on historical transaction data and engineered spatial features to deliver clean, confidence-building price predictions.

## Features

- **Intelligent Price Predictions:** Instantly evaluate property prices using:
  - **Basic Mode:** Quick estimates based on town, flat type, area, and remaining lease.
  - **Precise Mode:** Fine-grained, street-level accuracy incorporating full geolocations, layout configurations, and address-specific spatial features.
- **Dynamic Context-Rich Insights:** Receive personalized market insights alongside the valuation (e.g., price-per-sqm compared to the town average, lease decay metrics, and layout desirability).
- **Interactive UI & Fluid Experience:** A modern UI featuring data-forward visualizations, floating architectural aesthetics, and smooth transitions powered by Jinja2 and Tailwind-style utility classes.
- **Prediction History & Accounts:** Secure user authentication allowing users to save their predictions, clear history, and browse past valuations through the dashboard.
- **RESTful API:** Developer-friendly JSON endpoints (`/api/predict` and `/api/history`) for programmatic automated valuations.
- **Automated Testing Suite:** End-to-end testing components using `pytest` to validate application routing, authentication, and machine learning inference logic.

## Architecture & Technology Stack

- **Backend Framework:** Python / Flask
- **Machine Learning:** Scikit-Learn (`joblib`), XGBoost, pandas, NumPy
- **Database:** SQLite (with automated `init_db()` setup)
- **Frontend / UI:** HTML5, CSS3, Tailwind-style layouts, Jinja2 Templating
- **Testing environment:** `pytest` 

## Directory Structure

```text
├── app/
│   ├── ml/             # Preprocessing logic and cached Random Forest models
│   ├── models/         # Database models/schema abstraction handlers
│   ├── routes/         # Blueprints for Main UI, Authentication, and REST API
│   ├── templates/      # Jinja2 frontend layouts and web interface
│   ├── tests/          # Pytest suite 
│   ├── utils/          # Auxiliary scripts (e.g. input validators)
│   ├── app.py          # Flask application factory
│   ├── config.py       # Application configurations
│   ├── database.py     # SQLite initialization logic
├── env/                # Virtual environment wrapper (if initialized locally)
├── requirements.txt    # Python package dependencies
├── run.py              # Application entry point/server script
└── README.md           # This project documentation
```

## Installation & Setup

1. **Clone the repository and set up your workspace:**
   ```bash
   git clone <repository-url>
   cd ca1-daaa2b04-2423708-andrewpang
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python -m venv env
   # On Windows (PowerShell):
   .\env\Scripts\activate
   # On macOS / Linux:
   source env/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Based on your environment, you may need to resolve any specific platform binary requirements for heavy libraries like Scipy, XGBoost, and Scikit-Learn).*

4. **Launch the Application Server:**
   ```bash
   python run.py
   ```
   The local SQLite database (`prediction_history.db`) automatically initializes during the `create_app()` lifecycle flow structure.

5. **Access the application:**
   Open your browser and navigate to `http://localhost:5000` or `http://0.0.0.0:5000`.

6. **Run Automated Tests (Optional):**
   ```bash
   python -m pytest app/tests/
   ```

## Usage

### 1. Web Interface (Dashboard)
Navigate to `http://localhost:5000/predict` and use the interactive form. Select between "Basic Mode" for quick, general estimates or "Precise Mode" to feed in an exact address and retrieve location-aware ML insights.

### 2. Standard REST API Integration
To query predictions directly from the inference models, send a POST request to the API:

**Request (`POST /api/predict`):**
```bash
curl -X POST http://localhost:5000/api/predict \
     -H "Content-Type: application/json" \
     -d '{
       "mode": "basic",
       "town": "ANG MO KIO",
       "flat_type": "4 ROOM",
       "floor_area_sqm": "90",
       "remaining_lease": "85"
     }'
```

**JSON Response format:**
```json
{
  "mode": "basic",
  "prediction": 485000.0
}
```

## Credits
Developed for DOAA CA1 (Data Operations and Analytics Application - Continuous Assessment) by Andrew Pang.
