from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from .extensions import db
from src.backend.app.models import User, Account, Category, Goal, Bill, Transaction

# handle user sessions -- tracking who is logged in
login_manager = LoginManager()

# redirects to login if not authenticated
login_manager.login_view = 'auth.login'  

def create_app(test_config=None):
    # Creates and configures the Flask app

    app = Flask(__name__,
        # Points Flask to fronttend folder for html templates
        template_folder='../../frontend/templates',
        # Points Flask to frontend folder for static files
        static_folder='../../frontend/static'
    )

    if test_config is None:
        # Load the normal MySQL config from config.py
        app.config.from_object(Config)
    else:
        # Load the test settings (SQLite) instead
        app.config.update(test_config)

    # Initializes SQLAlchemy and Flask-Login with app 
    db.init_app(app)

    # CLI command to initialize the database
    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Database tables created.")

    # TEMP COMMENT OUT
    # login_manager.init_app(app)

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