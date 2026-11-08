from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from app.services import budget_service

budget = Blueprint("budget", __name__)

def today():
    return datetime.now(ZoneInfo("Asia/Manila")).date()

def valid_amount(value):
    try:
        amount = Decimal(value)

        if not amount.is_finite() or amount <= 0:
            return None

        if amount > Decimal("99999999.99"):
            return None

        return amount.quantize(Decimal("0.01"))

    except (InvalidOperation, TypeError, ValueError):
        return None

def error(message, status=400):
    return jsonify({"success": False, "message": message}), status

@budget.route("/budget")
def budget_page():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    budget_date = today()

    daily_budget = budget_service.get_daily_budget(
        user_id, budget_date)

    expenses = []
    summary = None
    if daily_budget:
        expenses = budget_service.get_daily_expenses(
            daily_budget["id"], user_id
        )

        summary = budget_service.get_budget_summary(
            daily_budget["id"], user_id
        )

    return render_template(
        "budget/budget.html",
        daily_budget=daily_budget,
        expenses=expenses,
        summary=summary
    )

@budget.route("/budget/create", methods=["POST"])
def create_budget():
    if "user_id" not in session:
        return error("Please log in again.", 401)

    amount = valid_amount(request.form.get("amount"))

    if amount is None:
        return error("Enter a valid budget amount.")

    user_id = session["user_id"]
    budget_date = today()

    if budget_service.get_daily_budget(user_id, budget_date):
        return error("Today's budget already exists.")

    budget_service.create_daily_budget(
        user_id, amount, budget_date
    )
    return jsonify({"success": True})


@budget.route("/budget/update", methods=["POST"])
def edit_budget():
    if "user_id" not in session:
        return error("Please log in again.", 401)

    amount = valid_amount(request.form.get("amount"))

    if amount is None:
        return error("Enter a valid budget amount.")

    daily_budget = budget_service.get_daily_budget(
        session["user_id"], today()
    )

    if not daily_budget:
        return error("Today's budget does not exist.", 404)

    updated = budget_service.update_daily_budget(
        session["user_id"], daily_budget["id"], amount
    )

    if not updated:
        return error("Unable to update budget.", 404)

    return jsonify({"success": True})

@budget.route("/budget/expense/add", methods=["POST"])
def create_expense():
    if "user_id" not in session:
        return error("Please log in again.", 401)

    user_id = session["user_id"]
    daily_budget = budget_service.get_daily_budget(user_id, today())

    if not daily_budget:
        return error("Set your budget first.")

    title = request.form.get("title", "").strip()
    details = request.form.get("details", "").strip()
    amount = valid_amount(request.form.get("amount"))

    if not title or len(title) > 100:
        return error("Expense title is required (maximum 100 characters).")

    if amount is None:
        return error("Enter a valid expense amount.")

    if len(details) > 5000:
        return error("Expense details are too long.")

    success = budget_service.add_expense(
        user_id, daily_budget["id"], title, amount, details
    )
    if not success:
        return error("Unable to add expense.", 404)

    return jsonify({"success": True})

@budget.route("/budget/expense/update", methods=["POST"])
def edit_expense():
    if "user_id" not in session:
        return error("Please log in again.", 401)

    expense_id = request.form.get("expense_id", type=int)

    if not expense_id:
        return error("Invalid expense.")

    title = request.form.get("title", "").strip()
    details = request.form.get("details", "").strip()
    amount = valid_amount(request.form.get("amount"))

    if not title or len(title) > 100:
        return error("Enter a valid expense title.")

    if amount is None:
        return error("Enter a valid expense amount.")

    if len(details) > 5000:
        return error("Expense details are too long.")

    success = budget_service.update_expense(
        session["user_id"], expense_id, title, amount, details
    )
    if not success:
        return error("Expense not found.", 404)

    return jsonify({"success": True})

@budget.route("/budget/expense/delete", methods=["POST"])
def remove_expense():
    if "user_id" not in session:
        return error("Please log in again.", 401)

    expense_id = request.form.get("expense_id", type=int)

    if not expense_id:
        return error("Invalid expense.")

    success = budget_service.delete_expense(
        session["user_id"], expense_id
    )

    if not success:
        return error("Expense not found.", 404)

    return jsonify({"success": True})
