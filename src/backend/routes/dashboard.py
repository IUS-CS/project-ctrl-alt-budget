from flask import Blueprint, render_template
from flask_login import login_required

dashboard_bp = Blueprint('dashboard', __name__)

# GET /dashboard - renders the dashboard template
# Shows user an overview of their financials 
@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
