from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()

# handle user sessions -- tracking who is logged in
login_manager = LoginManager()

# redirects to login if not authenticated
login_manager.login_view = 'auth.login'  

def create_app():
    # Creates and configures the Flask app

    app = Flask(__name__,
        # Points Flask to fronttend folder for html templates
        template_folder='../../frontend/templates',
        # Points Flask to frontend folder for static files
        static_folder='../../frontend/static'
    )

    # Loads in all settings from Config class in config.py
    app.config.from_object(Config)

    # Initializes SQLAlchemy and Flask-Login with app 
    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from ..routes.auth import auth_bp
    from ..routes.main import main_bp
    from ..routes.dashboard import dashboard_bp
    from ..routes.expenses import expenses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expenses_bp)

    return app