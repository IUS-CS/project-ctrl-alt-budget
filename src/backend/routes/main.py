from flask import Blueprint, render_template
from flask_login import login_required
# Blueprint homepage and other interactive non-auth or login related pages
main_bp = Blueprint('main', __name__)

# GET / = renders homepage template
@main_bp.route("/")
def home():
    return render_template("homepage.html")

@main_bp.route("/goals")
@login_required
def goals():
    return render_template("goals.html")

@main_bp.route("/reports")
@login_required
def reports():
    return render_template("reports.html")
