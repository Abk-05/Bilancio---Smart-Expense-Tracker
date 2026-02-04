from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from backend import db_helper
from logging_setup import setup_logger

# 1. Logger Setup
logger = setup_logger("fastapi_app")

# 2. App Start
app = FastAPI()

# 3. Data Models
class ExpenseCreate(BaseModel):
    expense_date: date
    category: str
    sub_category: str
    transaction_type: str
    amount: float

class ExpenseUpdate(BaseModel):
    expense_date: date
    category: str
    sub_category: str
    transaction_type: str
    amount: float

# --- ADD EXPENSE (POST) ---
@app.post("/expenses")
def add_expense(expense: ExpenseCreate):
    logger.info(f"POST /expenses called | Data: {expense.dict()}")
    try:
        db_helper.add_expense(
            expense.expense_date,
            expense.category,
            expense.sub_category,
            expense.transaction_type,
            expense.amount
        )
        logger.info("Expense added successfully")
        return {"message": "Expense added successfully"}
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        raise HTTPException(status_code=500, detail="Failed to add expense")

# --- FETCH ALL (GET) ---
@app.get("/expenses")
def get_all_expenses():
    logger.info("GET /expenses called")
    data = db_helper.show_all_expenses()
    logger.info(f"Returning {len(data)} expenses")
    return data

# --- SEARCH ENDPOINTS ---
@app.get("/expenses/id/{expense_id}")
def get_by_id(expense_id: int):
    logger.info(f"GET /expenses/id/{expense_id} called")
    data = db_helper.search_by_id(expense_id)
    if not data:
        logger.warning(f"Expense ID {expense_id} not found")
        raise HTTPException(status_code=404, detail="Expense not found")
    return data

@app.get("/expenses/category/{category}")
def get_by_category(category: str):
    logger.info(f"GET /expenses/category/{category} called")
    return db_helper.search_by_category(category)

@app.get("/expenses/subcategory/{sub_category}")
def get_by_subcategory(sub_category: str):
    logger.info(f"GET /expenses/subcategory/{sub_category} called")
    return db_helper.search_by_sub_category(sub_category)

@app.get("/expenses/type/{transaction_type}")
def get_by_type(transaction_type: str):
    logger.info(f"GET /expenses/type/{transaction_type} called")
    return db_helper.search_by_transaction_type(transaction_type)

# --- FILTER ENDPOINTS ---
@app.get("/expenses/filter/date_range")
def filter_date(start_date: date, end_date: date):
    logger.info(f"GET /expenses/filter/date_range called | {start_date} to {end_date}")
    return db_helper.filter_by_date_range(start_date, end_date)

@app.get("/expenses/filter/amount_range")
def filter_amount(min_amount: float, max_amount: float):
    logger.info(f"GET /expenses/filter/amount_range called | {min_amount} to {max_amount}")
    return db_helper.filter_by_amount_range(min_amount, max_amount)

# --- TOTALS / ANALYTICS ---
@app.get("/summary/today")
def total_today():
    logger.info("GET /summary/today called")
    total = db_helper.total_expense_today()
    return {"total_expense_today": total}

@app.get("/summary/month")
def total_month():
    logger.info("GET /summary/month called")
    total = db_helper.total_expense_this_month()
    return {"total_expense_this_month": total}

@app.get("/summary/year-wise")
def total_by_year():
    logger.info("GET /summary/year-wise called")
    return db_helper.total_expense_by_year()

# --- UPDATE (PUT) ---
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: ExpenseUpdate):
    logger.info(f"PUT /expenses/{expense_id} called | New Data: {expense.dict()}")
    try:
        db_helper.update_expense(
            expense_id,
            expense.expense_date,
            expense.category,
            expense.sub_category,
            expense.transaction_type,
            expense.amount
        )
        logger.info(f"Expense ID {expense_id} updated successfully")
        return {"message": "Expense updated successfully"}
    except Exception as e:
        logger.error(f"Error updating expense {expense_id}: {e}")
        raise HTTPException(status_code=500, detail="Update failed")

# --- DELETE (DELETE) ---
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    logger.info(f"DELETE /expenses/{expense_id} called")
    try:
        db_helper.delete_expense(expense_id)
        logger.info(f"Expense ID {expense_id} deleted successfully")
        return {"message": "Expense deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting expense {expense_id}: {e}")
        raise HTTPException(status_code=500, detail="Delete failed")