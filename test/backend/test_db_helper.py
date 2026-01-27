import pytest
from backend import db_helper
from datetime import date


def test_add_expense():
    # 1. यूनिक नाम इस्तेमाल करें ताकि पुराना डेटा बीच में न आए
    unique_name = "Test_Unique_Food"

    # 2. डेटा जोड़ो
    db_helper.add_expense("2024-01-01", unique_name, "papa", "debit", 1600)

    # 3. उसी यूनिक नाम से सर्च करो
    expenses = db_helper.search_by_category(unique_name)

    # 4. अब टेस्ट पक्का पास होगा
    assert len(expenses) > 0
    assert expenses[0]['category'] == unique_name
    assert float(expenses[0]['debit_or_credit']) == 1600.0