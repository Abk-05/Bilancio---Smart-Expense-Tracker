@echo off
echo ==================================================
echo Bilancio Expense Tracker - Setup & Launch
echo ==================================================
echo.

echo [Step 1] Checking & Installing Requirements...
pip install -r requirements.txt

echo.
echo [Step 2] Launching the App...
echo.
streamlit run frontend/app.py

pause