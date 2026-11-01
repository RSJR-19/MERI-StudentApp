from flask import Blueprint, render_template, redirect, url_for, session

main = Blueprint("main", __name__)

@main.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    return redirect(url_for("main.splash", destination="login"))

@main.route("/splash/<destination>")
def splash(destination):
    if destination not in ["login", "signup"]:
        return redirect(url_for("main.splash", destination="login"))

    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    return render_template( "splash/splash.html", destination=destination)

@main.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("main.splash", destination="login"))

    return render_template("dashboard/dashboard.html",first_name=session["first_name"])