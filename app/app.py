from flask import Flask
from app.config import Config
from app.database import init_db
from app.routes.main_routes import main_bp
from app.routes.auth_routes import auth_bp
from app.routes.api_routes import api_bp

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  # Initialize SQLite database
  init_db(app)

  # Register blueprints
  app.register_blueprint(main_bp)
  app.register_blueprint(auth_bp)
  app.register_blueprint(api_bp, url_prefix="/api")

  return app

app = create_app()
