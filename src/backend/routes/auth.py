from flask import Blueprint

# Blueprint groups all authentication related routes together
auth_bp = Blueprint('auth', __name__)

# GET /login - shows the login page
@app.route("/login")
def login():
    return "<h1>Login page coming soon</h1>"

# Get /signup - shows signup page
@app.route("/signup")
def signup():
    return "<h1>Signup page coming soon</h1>"