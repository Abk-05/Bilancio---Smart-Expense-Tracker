import pytest
from backend import db_helper
from datetime import date


def test_add_expense_visible():
    # 1. आज की तारीख (ताकि सबसे ऊपर आए)
    today = str(date.today())  # "2026-02-02"
    unique_name = "TEST_FINAL_CHECK"

    # 2. जोड़ा
    db_helper.add_expense(today, unique_name, "Self", "Expense", 6000.0)

    # 3. चेक किया (Assert)
    expenses = db_helper.search_by_category(unique_name)
    assert len(expenses) > 0


    id_to_delete = expenses[0]['id']
    db_helper.delete_expense(id_to_delete)

    print("✅ डेटा जुड़ गया! अब ऐप में जाकर रिफ्रेश करो।")