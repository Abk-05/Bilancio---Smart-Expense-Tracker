import mysql.connector
from contextlib import contextmanager
from datetime import datetime, date
from logging_setup import setup_logger


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
        raise err
    finally:
        cursor.close()
        connection.close()

# --- INSERT ---
def add_expense(expense_date, category, sub_category, transaction_type, amount):
    logger.info(f"Adding Expense: Date={expense_date}, Category={category},Sub_category={sub_category},transaction_type ={transaction_type} Amount={amount}")
    try:
        with get_connection() as cursor:
            query = """INSERT INTO expense(expense_date, category, sub_category, transaction_type, amount)
                     VALUES(%s, %s, %s, %s, %s)"""
            cursor.execute(query, (expense_date, category, sub_category, transaction_type, amount))
            logger.info("✅ Expense added successfully")
    except Exception as e:
        logger.error(f"❌ Failed to add expense: {e}")

# --- FETCH ALL ---
def show_all_expenses():
    logger.info("Fetching all expenses...")
    with get_connection() as cursor:
        query = "SELECT * FROM expense ORDER BY expense_date DESC, id DESC"
        cursor.execute(query)
        results = cursor.fetchall()
        logger.info(f"Total expenses fetched: {len(results)}")
        return results

# --- SEARCH FUNCTIONS ---
def search_by_id(expense_id):
    logger.info(f"Searching expense by ID: {expense_id}")
    with get_connection() as cursor:
        query = "SELECT * FROM expense WHERE id=%s"
        cursor.execute(query, (expense_id,))
        result = cursor.fetchone()
        if result:
            logger.info("✅ Record found")
        else:
            logger.warning(f"⚠️ No record found for ID: {expense_id}")
        return result

def search_by_category(category):
    logger.info(f"Searching by Category: {category}")
    with get_connection() as cursor:
        query = "SELECT * FROM expense WHERE category=%s ORDER BY expense_date DESC"
        cursor.execute(query, (category,))
        results = cursor.fetchall()
        logger.info(f"Found {len(results)} records for category '{category}'")
        return results

def search_by_sub_category(sub_category):
    logger.info(f"Searching by Sub-Category: {sub_category}")
    with get_connection() as cursor:
        query = "SELECT * FROM expense WHERE sub_category LIKE %s ORDER BY expense_date DESC"
        cursor.execute(query, (f"%{sub_category}%",))
        results = cursor.fetchall()
        logger.info(f"Found {len(results)} records for sub-category '{sub_category}'")
        return results


def search_by_transaction_type(transaction_type):
    logger.info(f"Searching by Transaction Type: {transaction_type}")
    with get_connection() as cursor:
        # SQL Query में LOWER() और TRIM() लगाया है (ताकि case sensitivity की दिक्कत न हो)
        query = "SELECT * FROM expense WHERE LOWER(TRIM(transaction_type)) = LOWER(TRIM(%s)) ORDER BY expense_date DESC"

        cursor.execute(query, (transaction_type,))
        results = cursor.fetchall()
        logger.info(f"Found {len(results)} records for type '{transaction_type}'")
        return results

# --- FILTERS ---
def filter_by_date_range(start_date, end_date):
    logger.info(f"Filtering by Date Range: {start_date} to {end_date}")
    with get_connection() as cursor:
        query = """
        SELECT * FROM expense
        WHERE expense_date BETWEEN %s AND %s
        ORDER BY expense_date DESC
        """
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()
        logger.info(f"Found {len(results)} records in date range")
        return results

def filter_by_amount_range(min_amount, max_amount):
    logger.info(f"Filtering by Amount: {min_amount} to {max_amount}")
    with get_connection() as cursor:
        query = """
        SELECT * FROM expense
        WHERE amount BETWEEN %s AND %s
        ORDER BY amount DESC
        """
        cursor.execute(query, (min_amount, max_amount))
        results = cursor.fetchall()
        logger.info(f"Found {len(results)} records in amount range")
        return results

# --- TOTALS ---
def total_expense_today():
    logger.info("Calculating total expense for TODAY")
    today = datetime.today().date()
    with get_connection() as cursor:
        query = """SELECT SUM(amount) as today_total FROM expense 
                   WHERE expense_date = %s AND transaction_type = 'Expense'"""
        cursor.execute(query, (today,))
        data = cursor.fetchone()
        total = float(data["today_total"]) if data and data["today_total"] else 0.0
        logger.info(f"Today's Total: {total}")
        return total

def total_expense_this_month():
    logger.info("Calculating total expense for THIS MONTH")
    today = date.today()
    first_day = today.replace(day=1)
    with get_connection() as cursor:
        query = """SELECT SUM(amount) as month_total FROM expense 
                   WHERE expense_date BETWEEN %s AND %s
                   AND transaction_type = 'Expense'"""
        cursor.execute(query, (first_day, today))
        data = cursor.fetchone()
        total = float(data["month_total"]) if data and data["month_total"] else 0.0
        logger.info(f"Month's Total: {total}")
        return total

def total_expense_by_year():
    logger.info("Calculating total expense by YEAR")
    with get_connection() as cursor:
        query = """
        SELECT YEAR(expense_date) AS year, SUM(amount) AS total
        FROM expense
        WHERE transaction_type = 'Expense'
        GROUP BY YEAR(expense_date)
        ORDER BY year DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        logger.info(f"Yearly data fetched for {len(results)} years")
        return results

# --- UPDATE & DELETE ---
def update_expense(id, expense_date, category, sub_category, transaction_type, amount):
    logger.info(f"Updating Expense ID: {id} | New Data: {amount}, {category}")
    try:
        with get_connection() as cursor:
            query = """UPDATE expense
                       SET expense_date=%s, category=%s, sub_category=%s, 
                           transaction_type=%s, amount=%s
                       WHERE id=%s"""
            cursor.execute(query, (expense_date, category, sub_category, transaction_type, amount, id))
            logger.info(f"✅ Expense ID {id} updated successfully")
    except Exception as e:
        logger.error(f"❌ Failed to update expense {id}: {e}")

def delete_expense(id):
    logger.info(f"Deleting Expense ID: {id}")
    try:
        with get_connection() as cursor:
            query = "DELETE FROM expense WHERE id=%s"
            cursor.execute(query, (id,))
            logger.info(f"✅ Expense ID {id} deleted successfully")
    except Exception as e:
        logger.error(f"❌ Failed to delete expense {id}: {e}")