from flask import Blueprint, request, redirect, render_template, session, flash, url_for
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

# -----------------------
# REGISTER
# -----------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    # Missing fields
    if not username or not password:
      flash("Please fill out all fields.", "register_general_error")
      return redirect(url_for("auth.register"))

    # Username exists
    if User.find_by_username(username):
      flash("Username already exists.", "register_username_error")
      return redirect(url_for("auth.register"))

    # Create new user
    User.create(username, password)
    flash("Account created successfully! Please log in.", "register_success")
    return redirect(url_for("auth.login"))

  return render_template("register.html")


# -----------------------
# AJAX: Username availability check
# -----------------------
@auth_bp.route("/api/check_username")
def api_check_username():
  username = request.args.get("username", "").strip()

  if not username:
    return {"exists": False}

  record = User.find_by_username(username)
  return {"exists": record is not None}


# -----------------------
# LOGIN
# -----------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    # Missing username
    if not username:
      flash("Please enter your username.", "login_username_error")
      return redirect(url_for("auth.login"))

    # Missing password
    if not password:
      flash("Please enter your password.", "login_password_error")
      return redirect(url_for("auth.login"))

    # Find user record manually
    record = User.find_by_username(username)

    # Username does not exist
    if record is None:
      flash("Username does not exist.", "login_username_error")
      return redirect(url_for("auth.login"))

    user_id, _, hashed_pw = record

    # Wrong password
    from werkzeug.security import check_password_hash
    if not check_password_hash(hashed_pw, password):
      flash("Incorrect password.", "login_password_error")
      return redirect(url_for("auth.login"))

    # Success
    session["user_id"] = user_id
    session["username"] = username
    flash("Logged in successfully!", "login_success")
    return redirect(url_for("main.index"))

  return render_template("login.html")


# -----------------------
# LOGOUT
# -----------------------
@auth_bp.route("/logout")
def logout():
  session.clear()
  flash("Logged out.", "logout_success")
  return redirect(url_for("auth.login"))
