from flask import Flask
from .config import Config
from .extensions import db, login_manager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to continue."
login_manager.login_message_category = "warning"


def create_app(test_config=None):
    # Creates and configures the Flask app

def create_app(test_config=None):
    app = Flask(__name__,
        template_folder='../../frontend/templates',
        static_folder='../../frontend/static'
    )

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import models so db.create_all() knows about them
    from .models import User, Account, Category, Goal, Bill, Transaction

    # CLI command to initialize the database
    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Database tables created.")

    # Import and register blueprints
    from src.backend.routes.auth import auth_bp
    from src.backend.routes.main import main_bp
    from src.backend.routes.dashboard import dashboard_bp
    from src.backend.routes.expenses import expenses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expenses_bp)

    return app