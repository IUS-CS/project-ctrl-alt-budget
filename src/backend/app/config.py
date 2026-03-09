import os 
from dotenv import load_dotenv

load_dotenv()

class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI =( 
        os.environ.get('DATABASE_URL') or 
        'mysql+pymysql://root:password@localhost/ctrl_alt_budget'                       
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    print("DB URL:", SQLALCHEMY_DATABASE_URI)