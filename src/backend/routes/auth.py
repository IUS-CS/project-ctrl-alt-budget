from uuid import uuid4

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import UserMixin, login_user, logout_user
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

from src.backend.app import db, login_manager

auth_bp = Blueprint("auth", __name__)


class LoginUser(UserMixin):
    def __init__(self, user_id, email, display_name=None):
        self.id = str(user_id)
        self.email = email
        self.display_name = display_name or email


@login_manager.user_loader
def load_user(user_id):
    query = text("""
        SELECT user_id, email, display_name
        FROM users
        WHERE user_id = :user_id
        LIMIT 1
    """)
    row = db.session.execute(query, {"user_id": user_id}).mappings().first()

    if not row:
        return None

    return LoginUser(row["user_id"], row["email"], row["display_name"])


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("login.html")

        query = text("""
            SELECT user_id, email, password_hash, display_name
            FROM users
            WHERE email = :email
            LIMIT 1
        """)
        user_row = db.session.execute(query, {"email": email}).mappings().first()

        if not user_row or not check_password_hash(user_row["password_hash"], password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        login_user(
            LoginUser(
                user_row["user_id"],
                user_row["email"],
                user_row["display_name"]
            )
        )
        flash("Logged in successfully.", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
@auth_bp.route("/register", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("signup.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("signup.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "danger")
            return render_template("signup.html")

        existing_user = db.session.execute(
            text("SELECT user_id FROM users WHERE email = :email LIMIT 1"),
            {"email": email},
        ).first()

        if existing_user:
            flash("An account with that email already exists.", "danger")
            return render_template("signup.html")

        user_id = str(uuid4())
        password_hash = generate_password_hash(password)

        insert_query = text("""
            INSERT INTO users (user_id, email, password_hash, display_name)
            VALUES (:user_id, :email, :password_hash, :display_name)
        """)

        db.session.execute(
            insert_query,
            {
                "user_id": user_id,
                "email": email,
                "password_hash": password_hash,
                "display_name": display_name or None,
            },
        )
        db.session.commit()

        login_user(LoginUser(user_id, email, display_name))
        flash("Account created successfully.", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("signup.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))