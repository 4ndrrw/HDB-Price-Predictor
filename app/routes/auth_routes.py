from flask import Blueprint, request, redirect, render_template, session, flash, url_for
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

# -----------------------
# REGISTER
# -----------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validation
        if not username or not password:
            flash("All fields required.")
            return redirect(url_for("auth.register"))

        if User.find_by_username(username):
            flash("Username already exists.")
            return redirect(url_for("auth.register"))

        # Create user
        User.create(username, password)

        flash("Account created successfully! Please log in.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# -----------------------
# LOGIN
# -----------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_id = User.verify(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            flash("Logged in successfully!")
            return redirect(url_for("main.index"))

        flash("Invalid username or password.")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


# -----------------------
# LOGOUT
# -----------------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("auth.login"))
