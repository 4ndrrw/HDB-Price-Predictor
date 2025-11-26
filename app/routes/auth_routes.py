from flask import Blueprint, render_template, request, redirect, session
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.authenticate(username, password):
            session["user"] = username
            return redirect("/")
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")
