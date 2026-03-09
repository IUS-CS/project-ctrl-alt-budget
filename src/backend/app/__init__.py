from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # redirects to login if not authenticated

def create_app(config_name='development'):
    app = Flask(__name__,
        template_folder='../../frontend/templates',
        static_folder='../../frontend/static'
    )

    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app