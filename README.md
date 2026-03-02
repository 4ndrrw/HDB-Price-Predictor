# 🏢 Precision Property Analytics - HDB Resale Price Predictor

## 📖 Overview

Precision Property Analytics is a machine-learning-powered Flask web application designed to predict the resale prices of Singapore Housing & Development Board (HDB) flats. The application offers two intuitive valuation modes—**Basic** and **Precise**—tailored to different use cases. It leverages regression models trained on historical transaction data and engineered spatial features to deliver clean, confidence-building price predictions.

## ✨ Features

- **Intelligent Price Predictions:** Instantly evaluate property prices using:
  - **Basic Mode:** Quick estimates based on town, flat type, area, and remaining lease.
  - **Precise Mode:** Fine-grained, street-level accuracy incorporating full geolocations, layout configurations, and address-specific spatial features.
- **Dynamic Context-Rich Insights:** Receive personalized market insights alongside the valuation (e.g., price-per-sqm compared to the town average, lease decay metrics, and layout desirability).
- **Interactive UI & Fluid Experience:** A modern UI featuring data-forward visualizations, floating architectural aesthetics, and smooth transitions powered by Jinja2 and Tailwind-style utility classes.
- **Prediction History & Accounts:** Secure user authentication allowing users to save their predictions, clear history, and browse past valuations through the dashboard.
- **RESTful API:** Developer-friendly JSON endpoints (`/api/predict` and `/api/history`) for programmatic automated valuations.
- **Automated Testing Suite:** End-to-end testing components using `pytest` to validate application routing, authentication, and machine learning inference logic.

## 🏗️ Architecture & Technology Stack

- **Backend Framework:** Python / Flask
- **Machine Learning:** Scikit-Learn (`joblib`), XGBoost, pandas, NumPy
- **Database:** SQLite (with automated `init_db()` setup)
- **Frontend / UI:** HTML5, CSS3, Tailwind-style layouts, Jinja2 Templating
- **Testing environment:** `pytest` 

## 📂 Directory Structure

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
