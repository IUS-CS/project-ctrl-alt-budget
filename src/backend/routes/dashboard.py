from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)

# GET /dashboard - renders the dashboard template
# Shows user an overview of their financials 
@dashboard_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
