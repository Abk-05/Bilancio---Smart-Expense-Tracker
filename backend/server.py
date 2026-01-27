from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List
from backend import db_helper
import logging
from backend.logging_setup import setup_logger

logger = setup_logger("fastapi_app")

app = FastAPI()

class ExpenseCreate(BaseModel):
    expense_date: date
    category: str
    sub_category: str
    transaction_type: str   # debit / credit
    debit_or_credit: float


class ExpenseUpdate(BaseModel):
    expense_date: date
    category: str
    sub_category: str
    transaction_type: str
    debit_or_credit: float

@app.post("/expenses")
def add_expense(expense: ExpenseCreate):
    logger.info(f"POST /expenses called | Data: {expense.dict()}")

    try:
        db_helper.add_expense(
            expense.expense_date,
            expense.category,
            expense.sub_category,
            expense.transaction_type,
            expense.debit_or_credit
        )
        logger.info("Expense added successfully")
        return {"message": "Expense added successfully"}
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        raise HTTPException(status_code=500, detail="Failed to add expense")

@app.get("/expenses")
def get_all_expenses():
    logger.info("GET /expenses called")
    data = db_helper.show_all_expenses()
    logger.info(f"Fetched {len(data)} expenses")
    return data

@app.get("/expenses/id/{expense_id}")
def get_by_id(expense_id: int):
    logger.info(f"GET /expenses/id/{expense_id} called")
    data = db_helper.search_by_id(expense_id)
    if not data:
        logger.warning(f"Expense not found with id={expense_id}")
        raise HTTPException(status_code=404, detail="Expense not found")

    logger.info(f"Expense found with id={expense_id}")
    return data

@app.get("/expenses/date/{expense_date}")
def get_by_date(expense_date: date):
    logger.info(f"GET /expenses/date/{expense_date} called")
    return db_helper.search_by_expense_date(expense_date)

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

@app.get("/expenses/filter/date_range")
def filter_date(start_date: date, end_date: date):
    logger.info(f"GET /expenses/filter/date_range called | {start_date} to {end_date}")
    return db_helper.filter_by_date_range(start_date, end_date)


@app.get("/expenses/filter/amount_range")
def filter_amount(min_amount: float, max_amount: float):
    logger.info(f"GET /expenses/filter/amount_range called | {min_amount} to {max_amount}")
    return db_helper.filter_by_amount_range(min_amount, max_amount)

@app.get("/summary/today")
def total_today():
    logger.info("GET /summary/today called")
    total = db_helper.total_expense_today()
    logger.info(f"Today's total expense: {total}")
    return {"total_expense_today": total}

@app.get("/summary/month")
def total_month():
    logger.info("GET /summary/month called")
    total = db_helper.total_expense_this_month()
    logger.info(f"This month's total expense: {total}")
    return {"total_expense_this_month": total}

@app.get("/summary/year-wise")
def total_by_year():
    logger.info("GET /summary/year-wise called")
    return db_helper.total_expense_by_year()

@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: ExpenseUpdate):
    logger.info(f"PUT /expenses/{expense_id} called | Data: {expense}")
    db_helper.update_expense(
        expense_id,
        expense.expense_date,
        expense.category,
        expense.sub_category,
        expense.transaction_type,
        expense.debit_or_credit
    )
    logger.info(f"Expense updated | id={expense_id}")
    return {"message": "Expense updated successfully"}

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    logger.info(f"DELETE /expenses/{expense_id} called")
    db_helper.delete_expense(expense_id)
    logger.info(f"Expense deleted | id={expense_id}")
    return {"message": "Expense deleted successfully"}
