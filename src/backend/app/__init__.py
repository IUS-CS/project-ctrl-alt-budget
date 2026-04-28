from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to continue."
login_manager.login_message_category = "warning"


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


    # CLI command to initialize the database
    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Database tables created.")



    # Initializes SQLAlchemy and Flask-Login with app 
    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from src.backend.routes.auth import auth_bp
    from src.backend.routes.main import main_bp
    from src.backend.routes.dashboard import dashboard_bp
    from src.backend.routes.expenses import expenses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expenses_bp)

    with app.app_context():
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                display_name TEXT
            )
        """))
        db.session.commit()


    return app