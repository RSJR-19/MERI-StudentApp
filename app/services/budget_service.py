from app.services.database import get_db_connection

def get_daily_budget(user_id, budget_date):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, budget_amount, budget_date
            FROM daily_budgets
            WHERE user_id = %s AND budget_date = %s
        """, (user_id, budget_date))

        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

def create_daily_budget(user_id, amount, budget_date):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO daily_budgets (user_id, budget_amount, budget_date)
            VALUES (%s, %s, %s)
        """, (user_id, amount, budget_date))

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def update_daily_budget(user_id, budget_id, amount):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id
            FROM daily_budgets
            WHERE id = %s
              AND user_id = %s
              AND budget_date = CURDATE()
        """, (budget_id, user_id))

        if not cursor.fetchone():
            return False

        cursor.execute("""
            UPDATE daily_budgets
            SET budget_amount = %s
            WHERE id = %s AND user_id = %s
              AND budget_date = CURDATE()
        """, (amount, budget_id, user_id))

        connection.commit()
        return True
    
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def get_daily_expenses(budget_id, user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT e.id, e.title, e.amount, e.details, e.created_at
            FROM expenses e
            INNER JOIN daily_budgets b ON e.budget_id = b.id
            WHERE e.budget_id = %s AND b.user_id = %s
            ORDER BY e.created_at ASC, e.id ASC
        """, (budget_id, user_id))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

def add_expense(user_id, budget_id, title, amount, details):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO expenses (budget_id, title, amount, details)
            SELECT id, %s, %s, %s
            FROM daily_budgets
            WHERE id = %s AND user_id = %s
              AND budget_date = CURDATE()
        """, (title, amount, details, budget_id, user_id))

        if cursor.rowcount == 0:
            connection.rollback()
            return False

        connection.commit()
        return True
    finally:
        cursor.close()
        connection.close()

def update_expense(user_id, expense_id, title, amount, details):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT e.id
            FROM expenses e
            INNER JOIN daily_budgets b ON e.budget_id = b.id
            WHERE e.id = %s
              AND b.user_id = %s
              AND b.budget_date = CURDATE()
            LIMIT 1
        """, (expense_id, user_id))

        expense = cursor.fetchone()

        if not expense:
            return False

        cursor.execute("""
            UPDATE expenses e
            INNER JOIN daily_budgets b ON e.budget_id = b.id
            SET e.title = %s,
                e.amount = %s,
                e.details = %s
            WHERE e.id = %s
              AND b.user_id = %s
              AND b.budget_date = CURDATE()
        """, (title, amount, details, expense_id, user_id))

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

def delete_expense(user_id, expense_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE e FROM expenses e
            INNER JOIN daily_budgets b ON e.budget_id = b.id
            WHERE e.id = %s
              AND b.user_id = %s
              AND b.budget_date = CURDATE()
        """, (expense_id, user_id))

        connection.commit()
        return cursor.rowcount > 0

    finally:
        cursor.close()
        connection.close()

def get_budget_summary(budget_id, user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                b.budget_amount,
                COALESCE(SUM(e.amount), 0) AS total_spent
            FROM daily_budgets b
            LEFT JOIN expenses e ON e.budget_id = b.id
            WHERE b.id = %s AND b.user_id = %s
            GROUP BY b.id, b.budget_amount
        """, (budget_id, user_id))

        result = cursor.fetchone()

        if result:
            result["remaining"] = (
                result["budget_amount"] - result["total_spent"]
            )

            result["percentage"] = min(
                float(result["total_spent"] / result["budget_amount"] * 100),
                100
            )

        return result

    finally:
        cursor.close()
        connection.close()
