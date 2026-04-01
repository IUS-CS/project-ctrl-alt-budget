from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from src.backend.db.models import db, User
import os

load_dotenv()

# Initializes and runs Flask app server

app = Flask(__name__)

# Database Engine Configuration
# in .env change DATABASE_URI=mysql+pymysql://user:password@localhost/budget_db to your dev credentials
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def home():

    # db test
    all_users = User.query.all()
    print(all_users)
    # Setup for route to homepage
    return "Budget App Backend Running"

if __name__ == "__main__":
    # Starts dev server in debug mode
    app.run(debug = True)