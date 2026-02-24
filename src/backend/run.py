from flask import Flask

# Initializes and runs Flask app server

app = Flask(__name__)

@app.route("/")
def home():
    # Setup for route to homepage
    return "Budget App Backend Running"

if __name__ == "__main__":
    # Starts dev server in debug mode
    app.run(debug = True)