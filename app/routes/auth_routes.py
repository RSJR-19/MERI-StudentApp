from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.services.auth_service import validate_signup,register_user, authenticate_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():

    if "user_id" in session:
        return redirect(url_for("main.dashboard"))


    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")


        if not email or not password:
            flash("Please complete all fields.")
            return redirect(url_for("auth.login"))
        
        success, user = authenticate_user(email, password)

        if success:
            session.clear()
            session["user_id"] = user["id"]
            session["first_name"] = user["first_name"]


            if request.form.get("remember") == "yes":
                session.permanent = True


            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password.")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if "user_id" in session:
        return redirect(url_for("main.dashboard"))


    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        valid, message = validate_signup(first_name, last_name, email, password, confirm_password)

        if not valid:
            flash(message)
            return redirect(url_for("auth.signup"))


        success, message = register_user(first_name, last_name, email, password)

        if success:
            success, user = authenticate_user(email, password)

        if success:
            session.clear()
            session["user_id"] = user["id"]
            session["first_name"] = user["first_name"]

            return redirect(url_for("main.dashboard"))

        flash(message)

        return redirect(url_for("auth.signup"))
    
    return render_template("auth/signup.html")


@auth.route("/logout")
def logout():
    session.clear()

    return redirect(
        url_for("main.splash", destination="login")
    )