import re
from werkzeug.security import generate_password_hash,check_password_hash
from mysql.connector import IntegrityError
from app.services.database import get_db_connection


def validate_signup(first_name, last_name, email, password, confirm_password):

    if not first_name or not last_name or not email or not password or not confirm_password:

        return False, "Please complete all fields."


    if len(first_name) > 50 or len(last_name) > 50:

        return False, "Names must not exceed 50 characters"


    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Please enter a valid email address."


    if len(email) > 254:
        return False, "Email address is too long."


    if len(password) < 8 or len(password) > 64:
        return False, "Password must be only 8-64 characters long."
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter."


    if not re.search(r"[a-z]", password):
        return False, "Password must contain a lowercase letter."


    if not re.search(r"[0-9]", password):
        return False, "Password must contain a number."


    if password != confirm_password:
        return False, "Passwords do not match."


    return True, "Validation successful."


def register_user(first_name, last_name, email, password):

    connection = get_db_connection()
    cursor = connection.cursor()
    password_hash = generate_password_hash(password)

    try:
        cursor.execute("INSERT INTO users (first_name, last_name, email, password_hash) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, password_hash))

        connection.commit()

        return True, "Account created successfully."

    except IntegrityError:
        connection.rollback()
        return False, "Email address is already registered"

    finally:
        cursor.close()
        connection.close()

def authenticate_user(email, password):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, first_name, last_name, email, password_hash FROM users WHERE email = %s",(email,))

        user = cursor.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            return True, user

        else:
            return False, None

    finally:
        cursor.close()
        connection.close()