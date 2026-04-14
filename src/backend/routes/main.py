from flask import Blueprint, render_template

# Blueprint homepage and other interactive non-auth or login related pages
main_bp = Blueprint('main', __name__)

# GET / = renders homepage template
@main_bp.route("/")
def home():
    return render_template("homepage.html")
