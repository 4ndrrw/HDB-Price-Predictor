from flask import Flask
from app.config import Config
from app.database import init_db
from app.routes.main_routes import main_bp
from app.routes.auth_routes import auth_bp
from app.routes.api_routes import api_bp


# -----------------------------
# Custom Jinja filter: format GBP with spaces
# -----------------------------
def format_gbp(value):
    try:
        value = float(value)
        # Format with commas, then replace with spaces → "1 234 567.89"
        return f"{value:,.2f}".replace(",", " ")
    except:
        return value


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLite database
    init_db(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Register Jinja filter
    app.jinja_env.filters["gbp"] = format_gbp

    return app


app = create_app()
