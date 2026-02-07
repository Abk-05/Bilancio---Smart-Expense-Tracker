<div align="center">

  <img src="frontend/logo.png" alt="logo" width="150" height="auto" />
  
  # 💸 Bilancio: Smart Expense Tracker

  <p>
    <b>Track. Analyze. Save.</b><br>
    A powerful tool to take control of your financial life.
  </p>

  <p>
    <a href="https://python.org">
      <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    </a>
    <a href="https://streamlit.io">
      <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
    </a>
    <a href="https://mysql.com">
      <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
    </a>
    <a href="https://pandas.pydata.org">
      <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
    </a>
  </p>

  <br>

  <img src="photos/charts.png" alt="Dashboard" width="100%" style="border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);">

</div>

---

## 📖 Overview

**Bilancio** is your personal financial assistant. Built with a robust **Python** backend and a responsive **Streamlit** frontend, it allows users to log daily transactions, visualize spending trends, and export reports with ease.

---

## ✨ Top Features

* **📊 Interactive Dashboard:** Visualize your spending with dynamic Pie Charts & Bar Graphs.
* **➕ Easy Entry:** Add Income/Expenses quickly with categories and notes.
* **🔎 Smart Search:** Filter transactions by Date Range, Category, or Amount.
* **🗑️ Secure Management:** Update or Delete wrong entries instantly.
* **💾 Data Export:** Download your financial history as a CSV file.

---

## 📸 Application Tour

<div align="center"> 
  <img src="photos/add.png" alt="Add Transaction" width="45%" style="margin-right: 10px;" />
  <img src="photos/Delete.png" alt="Delete Transaction" width="45%" />
  
  <br><br>

  <img src="photos/custom_data.png" alt="Filter Data" width="45%" style="margin-right: 10px;" />
  <img src="photos/update.png" alt="Update Data" width="45%" />
</div>

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | `Streamlit` | For building the interactive web UI. |
| **Backend** | `Python` | Handles logic, calculations, and routing. |
| **Database** | `MySQL` | Stores all transaction records securely. |
| **Visualization** | `Plotly/Pandas` | Powers the beautiful analytics charts. |

---

## 🚀 Quick Start Guide

**1. Clone the Repository**
```bash
git clone [https://github.com/Abk-05/Bilancio---Smart-Expense-Tracker.git](https://github.com/Abk-05/Bilancio---Smart-Expense-Tracker.git)
cd Bilancio---Smart-Expense-Tracker


## Setup Instructions

2.  **MySQL Server** (The database software) -> [Download Here](https://dev.mysql.com/downloads/installer/)
1. **Install dependencies:**:   
   ```commandline
    pip install -r requirements.txt
   ```
1. **Run the FastAPI server:**:   
   ```commandline
     python -m uvicorn backend.server:app --reload
   ```
1. **Run the Streamlit app:**:   
   ```commandline
    python -m streamlit run frontend/app.py

