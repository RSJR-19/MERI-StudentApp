import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from datetime import timedelta
from app.routes.budget_routes import budget

csrf = CSRFProtect()


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    csrf.init_app(app)

    from app.routes.main_routes import main
    from app.routes.auth_routes import auth
    

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(budget)

    return app