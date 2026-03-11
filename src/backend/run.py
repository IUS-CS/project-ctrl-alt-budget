from flask import Flask, render_template, jsonify, request

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

# temporary in-memory transaction list
transactions = [
    {"date": "2026-02-20", "desc": "Paycheck", "type": "INCOME", "amount": 500},
    {"date": "2026-02-21", "desc": "Rent", "type": "EXPENSE", "amount": 300},
    {"date": "2026-02-22", "desc": "Gas", "type": "EXPENSE", "amount": 45.5}
]

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login")
def login():
    return "<h1>Login page coming soon</h1>"

@app.route("/register")
def register():
    return "<h1>Register page coming soon</h1>"

@app.route("/signup")
def signup():
    return "<h1>Signup page coming soon</h1>"

@app.route("/expenses")
def expenses():
    return render_template("expenses.html")

@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    return jsonify(transactions)

@app.route("/api/transactions", methods=["POST"])
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

if __name__ == "__main__":
    app.run(debug=True)