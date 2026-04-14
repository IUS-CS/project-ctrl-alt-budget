from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required

expenses_bp = Blueprint('expenses', __name__)

# temporary in-memory transaction list
transactions = [
    {"date": "2026-02-20", "desc": "Paycheck", "type": "INCOME", "amount": 500},
    {"date": "2026-02-21", "desc": "Rent", "type": "EXPENSE", "amount": 300},
    {"date": "2026-02-22", "desc": "Gas", "type": "EXPENSE", "amount": 45.5}
]

# GET /expenses — renders the expenses page template
@expenses_bp.route("/expenses")
@login_required
def expenses():
    return render_template("expenses.html")

# GET /api/transactions — returns all transactions as JSON
# To be used by the frontend to fetch and display the transaction list
@expenses_bp.route("/api/transactions", methods=["GET"])
@login_required
def get_transactions():
    return jsonify(transactions)


# Unfinished -- Needs integrated with transaction class
# POST -- adds a new transaction to list
@expenses_bp.route("/api/transactions", methods=["POST"])
@login_required
def add_transaction():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["date", "desc", "type", "amount"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    transactions.insert(0, data)

    return jsonify({
        "message": "Transaction added successfully",
        "transaction": data
    }), 201
