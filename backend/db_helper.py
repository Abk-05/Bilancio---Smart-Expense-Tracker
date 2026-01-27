import mysql.connector
from contextlib import contextmanager
from datetime import datetime, date
from backend.logging_setup import setup_logger

logger = setup_logger('db_helper')

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "ankit_singh",
    "database": "expense"
}

@contextmanager
def get_connection():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
        logger.error(f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()

# --- INSERT ---
def add_expense(expense_date, category, sub_category, transaction_type, amount):
    logger.info(f"Adding: {expense_date}, {category}, {sub_category}, {transaction_type}, {amount}")
    with get_connection() as cursor:
        # Changed debit_or_credit -> amount
        query = """INSERT INTO expense(expense_date, category, sub_category, transaction_type, amount)
                 VALUES(%s, %s, %s, %s, %s)"""
        cursor.execute(query, (expense_date, category, sub_category, transaction_type, amount))
        logger.info("Expense added successfully")

# --- FETCH ALL ---
def show_all_expenses():
    with get_connection() as cursor:
        query = "SELECT * FROM expense ORDER BY expense_date DESC"
        cursor.execute(query)
        return cursor.fetchall()

# --- SEARCH FUNCTIONS ---
def search_by_id(expense_id):
    with get_connection() as cursor:
        query = "SELECT * FROM expense WHERE id=%s"
        cursor.execute(query, (expense_id,))
        return cursor.fetchone()

def search_by_category(category):
    with get_connection() as cursor:
        query = "SELECT * FROM expense WHERE category=%s ORDER BY expense_date DESC"
        cursor.execute(query, (category,))
        return cursor.fetchall()

def search_by_sub_category(sub_category):
    with get_connection() as cursor:
        query = "SELECT * FROM expense WHERE sub_category LIKE %s ORDER BY expense_date DESC"
        cursor.execute(query, (f"%{sub_category}%",))
        return cursor.fetchall()

def search_by_transaction_type(transaction_type):
    with get_connection() as cursor:
        query = "SELECT * FROM expense WHERE transaction_type=%s ORDER BY expense_date DESC"
        cursor.execute(query, (transaction_type,))
        return cursor.fetchall()

# --- FILTERS ---
def filter_by_date_range(start_date, end_date):
    with get_connection() as cursor:
        query = """
        SELECT * FROM expense
        WHERE expense_date BETWEEN %s AND %s
        ORDER BY expense_date DESC
        """
        cursor.execute(query, (start_date, end_date))
        return cursor.fetchall()

def filter_by_amount_range(min_amount, max_amount):
    with get_connection() as cursor:
        # Changed debit_or_credit -> amount
        query = """
        SELECT * FROM expense
        WHERE amount BETWEEN %s AND %s
        ORDER BY amount DESC
        """
        cursor.execute(query, (min_amount, max_amount))
        return cursor.fetchall()

# --- TOTALS ---
def total_expense_today():
    today = datetime.today().date()
    with get_connection() as cursor:
        # Changed SUM(debit_or_credit) -> SUM(amount)
        query = """SELECT SUM(amount) as today_total FROM expense 
                   WHERE expense_date = %s AND transaction_type = 'Expense'"""
        cursor.execute(query, (today,))
        data = cursor.fetchone()
        return float(data["today_total"]) if data and data["today_total"] else 0.0

def total_expense_this_month():
    today = date.today()
    first_day = today.replace(day=1)
    with get_connection() as cursor:
        # Changed SUM(debit_or_credit) -> SUM(amount)
        query = """SELECT SUM(amount) as month_total FROM expense 
                   WHERE expense_date BETWEEN %s AND %s
                   AND transaction_type = 'Expense'"""
        cursor.execute(query, (first_day, today))
        data = cursor.fetchone()
        return float(data["month_total"]) if data and data["month_total"] else 0.0

def total_expense_by_year():
    with get_connection() as cursor:
        # Changed SUM(debit_or_credit) -> SUM(amount)
        query = """
        SELECT YEAR(expense_date) AS year, SUM(amount) AS total
        FROM expense
        WHERE transaction_type = 'Expense'
        GROUP BY YEAR(expense_date)
        ORDER BY year DESC
        """
        cursor.execute(query)
        return cursor.fetchall()

# --- UPDATE & DELETE ---
def update_expense(id, expense_date, category, sub_category, transaction_type, amount):
    with get_connection() as cursor:
        # Changed debit_or_credit -> amount
        query = """UPDATE expense
                   SET expense_date=%s, category=%s, sub_category=%s, 
                       transaction_type=%s, amount=%s
                   WHERE id=%s"""
        cursor.execute(query, (expense_date, category, sub_category, transaction_type, amount, id))

def delete_expense(id):
    with get_connection() as cursor:
        query = "DELETE FROM expense WHERE id=%s"
        cursor.execute(query, (id,))