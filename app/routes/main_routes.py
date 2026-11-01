from flask import Blueprint, render_template, redirect, url_for, session

main = Blueprint("main", __name__)

@main.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("main.splash", destination="dashboard"))

    return redirect(url_for("main.splash", destination="login"))

@main.route("/splash/<destination>")
def splash(destination):
    if destination not in ["login", "signup", "dashboard"]:
        return redirect(url_for("main.splash", destination="login"))

    if destination == "dashboard" and "user_id" not in session:
        return redirect(url_for("main.splash", destination="login"))

    if destination in ["login", "signup"] and "user_id" in session:
        return redirect(url_for("main.splash", destination="dashboard"))

    return render_template( "splash/splash.html", destination=destination)

@main.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("main.splash", destination="login"))

    return render_template("dashboard/dashboard.html",first_name=session["first_name"])