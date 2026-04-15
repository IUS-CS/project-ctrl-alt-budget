from flask import Flask
from .config import Config
from .extensions import db, login_manager


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
    from ..routes.auth import auth_bp
    from ..routes.main import main_bp
    from ..routes.dashboard import dashboard_bp
    from ..routes.expenses import expenses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expenses_bp)

    return app