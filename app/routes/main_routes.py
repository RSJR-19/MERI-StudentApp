from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for

main = Blueprint("main", __name__)

@main.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("main.splash", destination="dashboard"))

    return redirect(url_for("main.splash", destination="login"))

@main.route("/splash/<destination>")
def splash(destination):

    allowed_destinations = [
        "login",
        "signup",
        "dashboard",
        "budget",
        "schedule"
    ]
    if destination not in allowed_destinations:
        return redirect(url_for("main.splash", destination="login"))
    
    if destination in ["dashboard", "budget", "schedule"] and "user_id" not in session:
        return redirect(url_for("main.splash", destination="login"))

    if destination in ["login", "signup"] and "user_id" in session:
        return redirect(url_for("main.splash", destination="dashboard"))

    return render_template(
        "splash/splash.html",
        destination=destination
    )

@main.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.splash", destination="login"))

    first_name = session.get("first_name", "")
    last_name = session.get("last_name", "")

    full_name = f"{first_name} {last_name}"
    initials = f"{first_name[:1]}{last_name[:1]}".upper()

    return render_template(
        "dashboard/dashboard.html",
        first_name=first_name,
        full_name=full_name,
        initials=initials
    )
