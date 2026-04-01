import os 
from dotenv import load_dotenv

# Loads environment variables from .env
load_dotenv()

class Config:
    # Used to encrypt sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # DB connection for SQLAlchemy, uses a default local connection if not set in .env
    SQLALCHEMY_DATABASE_URI =( 
        os.environ.get('DATABASE_URL') or 
        'mysql+pymysql://root:password@localhost/ctrl_alt_budget'                       
    )

    # Enables Flask debug mode - shows detailed error pages and auto reloads
    DEBUG = True