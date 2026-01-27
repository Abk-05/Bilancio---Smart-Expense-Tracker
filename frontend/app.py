import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import date
import sys
import os

# --- 1. Path Setup ---
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))

try:
    import db_helper
except ImportError:
    from backend import db_helper

# --- 2. Page Config ---
st.set_page_config(
    page_title="Bilancio - Smart Finance Tracker",
    layout="wide",
    page_icon="💰"
)

# ==========================================
# 🎨 CUSTOM CSS
# ==========================================
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 18px;
    }
    [data-testid="stSidebar"] * {
        font-size: 20px !important;
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stDateInput label, .stRadio label {
        font-size: 18px !important;
        font-weight: bold;
    }
    .stButton button {
        font-size: 20px !important;
        font-weight: bold;
        padding: 10px;
    }
    .credit-text {
        text-align: center;
        font-weight: bold;
        margin-top: 5px; 
        font-size: 16px !important;
        opacity: 0.9;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar Styling ---
with st.sidebar:
    logo_path = os.path.join(current_dir, "logo.jpg")

    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        alt_path_1 = os.path.join(current_dir, "logo.jpg.png")
        alt_path_2 = os.path.join(current_dir, "image (2).jpg")
        if os.path.exists(alt_path_1):
            st.image(alt_path_1, use_container_width=True)
        elif os.path.exists(alt_path_2):
            st.image(alt_path_2, use_container_width=True)
        else:
            st.markdown("## 💰 **Bilancio**")
            st.caption("Smart Finance Tracker")

    st.markdown("---")

    menu = st.radio(
        "📂 **Navigation**",
        [
            "➕ Add Transaction",
            "✏️ Update Transaction",
            "🗑️ Delete Transaction",
            "📋 View All Transactions",
            "🔍 Search by ID",
            "🏷️ Search by Category",
            "📝 Search by Sub Category",
            "💳 Search by Transaction Type",
            "🛠️ Custom Data Filter",
            "📊 Dashboard & Charts"
        ]
    )

    st.markdown('<p class="credit-text">Developed with ❤️ by Ankit</p>', unsafe_allow_html=True)


# --- 4. UNIVERSAL DOWNLOAD FUNCTION ---
def show_data_with_downloads(df, key_prefix=""):
    if df.empty:
        st.warning("⚠️ No Data Found.")
        return

    st.markdown("### 📄 Result Data")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.markdown("##### 📥 Download Report")

    c1, c2, c3 = st.columns([1, 1, 2])

    csv = df.to_csv(index=False).encode('utf-8')
    c1.download_button(
        label="📄 Download CSV",
        data=csv,
        file_name=f"Bilancio_Data_{key_prefix}.csv",
        mime="text/csv",
        key=f"csv_{key_prefix}"
    )

    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Bilancio - Report", styles['Title']))
    elements.append(Paragraph(f"Generated on: {date.today()}", styles['Normal']))
    elements.append(Paragraph(" ", styles['Normal']))

    # UPDATE: Changed 'debit_or_credit' to 'amount'
    standard_cols = ['id', 'expense_date', 'category', 'sub_category', 'transaction_type', 'amount']
    cols_to_print = [c for c in df.columns if c in standard_cols]

    if not cols_to_print:
        cols_to_print = df.columns.tolist()

    data_list = [cols_to_print] + df[cols_to_print].astype(str).values.tolist()

    t = Table(data_list)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgoldenrod),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10)
    ]))
    elements.append(t)
    doc.build(elements)

    c2.download_button(
        label="📄 Download PDF",
        data=pdf_buffer.getvalue(),
        file_name=f"Bilancio_Report_{key_prefix}.pdf",
        mime="application/pdf",
        key=f"pdf_{key_prefix}"
    )


# --- CHART GENERATOR HELPER ---
def generate_charts(df):
    st.markdown("---")

    df['type_calc'] = df['transaction_type'].astype(str).str.strip().str.lower()

    # UPDATE: Changed 'debit_or_credit' to 'amount'
    total_expense = df[df['type_calc'] == 'expense']['amount'].sum()
    total_income = df[df['type_calc'] == 'income']['amount'].sum()

    m1, m2 = st.columns(2)

    has_income = not df[df['type_calc'] == 'income'].empty
    has_expense = not df[df['type_calc'] == 'expense'].empty

    if has_income:
        m1.metric("Total Income", f"₹ {total_income:,.2f}")
    else:
        m1.metric("Total Income", "₹ 0.00")

    if has_expense:
        m2.metric("Total Expense", f"₹ {total_expense:,.2f}")
    else:
        m2.metric("Total Expense", "₹ 0.00")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Category Share")
        if not df.empty:
            # UPDATE: Changed 'debit_or_credit' to 'amount'
            fig_pie = px.pie(df, names='category', values='amount', hole=0.5,
                             color_discrete_sequence=px.colors.qualitative.Prism)
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No data for charts.")

    with c2:
        st.subheader("Transaction Trend")
        if not df.empty:
            # UPDATE: Changed 'debit_or_credit' to 'amount'
            daily = df.groupby('expense_date')['amount'].sum().reset_index()
            fig_bar = px.bar(daily, x='expense_date', y='amount', color='amount',
                             color_continuous_scale='Plasma')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No data for charts.")


# ================= MAIN APP HEADER =================
if menu == "➕ Add Transaction":
    st.title("➕ Bilancio: Add Transaction")
elif menu == "✏️ Update Transaction":
    st.title("✏️ Bilancio: Update Transaction")
elif menu == "🗑️ Delete Transaction":
    st.title("🗑️ Bilancio: Delete Transaction")
elif menu == "📋 View All Transactions":
    st.title("📋 Bilancio: All Transactions")
elif "Search" in menu:
    st.title(f"{menu.split(' by ')[-1]} Search")
elif "Filter" in menu:
    st.title("🛠️ Bilancio Custom Filter")
elif "Dashboard" in menu:
    st.title("📊 Bilancio Analytics Dashboard")

# ================= 1. ADD TRANSACTION =================
if menu == "➕ Add Transaction":
    def cb_add_expense():
        d = st.session_state.get('add_date')
        cat = st.session_state.get('add_cat')
        sub = st.session_state.get('add_sub')
        ttype = st.session_state.get('add_type')
        amt = st.session_state.get('add_amt')

        if not cat:
            st.error("❌ Please select a category!")
            return
        if amt <= 0:
            st.error("❌ Amount must be greater than 0!")
            return

        db_helper.add_expense(d, cat, sub, ttype, amt)
        st.toast("✅ Transaction Added Successfully!", icon="🎉")

        st.session_state['add_cat'] = None
        st.session_state['add_sub'] = ""
        st.session_state['add_amt'] = 0.0
        st.session_state['add_type'] = "Expense"


    with st.container(border=True):
        c1, c2 = st.columns(2)
        c1.date_input("📅 Date", date.today(), key='add_date')
        c1.selectbox("📂 Category",
                     ["Food", "Travel", "Bills", "Shopping", "Entertainment", "Salary", "Business", "Others"],
                     index=None, placeholder="Select...", key='add_cat')
        c1.text_input("📝 Sub Category", key='add_sub')
        c2.selectbox("💳 Type", ["Expense", "Income"], key='add_type')
        c2.number_input("💰 Amount", min_value=0.0, step=10.0, max_value=1000000000.0, key='add_amt')
        st.button("✅ Save Transaction", on_click=cb_add_expense, use_container_width=True)

# ================= 2. UPDATE TRANSACTION =================
elif menu == "✏️ Update Transaction":
    def cb_update_expense():
        uid = st.session_state.get('upd_search_id')
        ud = st.session_state.get('u_date')
        uc = st.session_state.get('u_cat')
        us = st.session_state.get('u_sub')
        ut = st.session_state.get('u_type')
        ua = st.session_state.get('u_amt')

        db_helper.update_expense(uid, ud, uc, us, ut, ua)
        st.toast(f"✅ Transaction {uid} Updated!", icon="🔄")

        st.session_state['update_found_data'] = None
        st.session_state['upd_search_id'] = 0


    st.markdown("Enter ID to edit details.")
    search_id = st.number_input("Enter Transaction ID", min_value=0, step=1, key='upd_search_id')

    if st.button("🔍 Fetch Details"):
        if search_id > 0:
            record = db_helper.search_by_id(search_id)
            if record:
                st.session_state['update_found_data'] = record
                st.success("Transaction Found!")
            else:
                st.error("ID Not Found.")
                st.session_state['update_found_data'] = None

    if st.session_state.get('update_found_data'):
        data = st.session_state['update_found_data']
        with st.container(border=True):
            st.markdown(f"**Editing Transaction ID: {data['id']}**")
            c1, c2 = st.columns(2)
            c1.date_input("📅 Date", data['expense_date'], key='u_date')
            opts_cat = ["Food", "Travel", "Bills", "Shopping", "Entertainment", "Salary", "Business", "Others"]
            idx_cat = opts_cat.index(data['category']) if data['category'] in opts_cat else 0
            c1.selectbox("📂 Category", opts_cat, index=idx_cat, key='u_cat')
            c1.text_input("📝 Sub Category", value=data['sub_category'], key='u_sub')
            opts_type = ["Expense", "Income"]
            idx_type = opts_type.index(data['transaction_type']) if data['transaction_type'] in opts_type else 0
            c2.selectbox("💳 Type", opts_type, index=idx_type, key='u_type')

            # UPDATE: Changed 'debit_or_credit' to 'amount'
            c2.number_input("💰 Amount", value=float(data['amount']), min_value=0.0, max_value=1000000000.0, key='u_amt')
            st.markdown("---")
            st.button("✅ Confirm Update", on_click=cb_update_expense, use_container_width=True)

# ================= 3. DELETE TRANSACTION =================
elif menu == "🗑️ Delete Transaction":
    def cb_delete_expense():
        did = st.session_state.get('del_id_input')
        if did > 0:
            rec = db_helper.search_by_id(did)
            if rec:
                db_helper.delete_expense(did)
                st.toast(f"✅ Transaction {did} Deleted!", icon="🗑️")
                st.session_state['del_id_input'] = 0
            else:
                st.error("ID Not Found!")
        else:
            st.error("Invalid ID")


    st.markdown("⚠️ **Warning:** This action cannot be undone.")
    st.number_input("Enter Transaction ID to Delete", min_value=0, step=1, key='del_id_input')
    st.button("🗑️ Delete Permanently", on_click=cb_delete_expense, type="primary")

# ================= 4. VIEW ALL =================
elif menu == "📋 View All Transactions":
    data = db_helper.show_all_expenses()
    show_data_with_downloads(pd.DataFrame(data), "all")

# ================= 6. SEARCH OPTIONS =================
elif menu == "🔍 Search by ID":
    sid = st.number_input("Enter Transaction ID", min_value=1, step=1)
    if st.button("Search"):
        data = db_helper.search_by_id(sid)
        if data:
            show_data_with_downloads(pd.DataFrame([data]), "id")
        else:
            st.error("Not Found")

elif menu == "🏷️ Search by Category":
    cat = st.selectbox("Category",
                       ["Food", "Travel", "Bills", "Shopping", "Entertainment", "Salary", "Business", "Others"])
    if st.button("Search"):
        data = db_helper.search_by_category(cat)
        show_data_with_downloads(pd.DataFrame(data), "cat")

elif menu == "📝 Search by Sub Category":
    st.markdown("Search for specific items like 'Pizza', 'Uber', 'Rent', etc.")
    sub_cat_input = st.text_input("Enter Sub Category")
    if st.button("Search Sub Category"):
        if sub_cat_input:
            data = db_helper.search_by_sub_category(sub_cat_input)
            df = pd.DataFrame(data)
            if not df.empty:
                st.success(f"Found {len(df)} records matching '{sub_cat_input}'")
                show_data_with_downloads(df, "sub_cat")
            else:
                st.warning(f"No records found for '{sub_cat_input}'")
        else:
            st.error("Please enter a sub category name.")

elif menu == "💳 Search by Transaction Type":
    tt = st.radio("Type", ["Expense", "Income"], horizontal=True)
    if st.button("Search"):
        data = db_helper.search_by_transaction_type(tt)
        if not data:
            all_data = db_helper.show_all_expenses()
            df = pd.DataFrame(all_data)
            if not df.empty:
                df['type_clean'] = df['transaction_type'].astype(str).str.strip().str.lower()
                df = df[df['type_clean'] == tt.lower()]
                show_data_with_downloads(df, "type_fallback")
            else:
                st.error("Not Found")
        else:
            show_data_with_downloads(pd.DataFrame(data), "type")

# ================= 9. CUSTOM FILTER (UNIVERSAL FIX) =================
elif menu == "🛠️ Custom Data Filter":
    st.markdown("Filter your Bilancio transactions:")

    tab_date, tab_amt = st.tabs(["📅 Filter by Date", "💰 Filter by Amount"])

    with tab_date:
        c1, c2 = st.columns(2)
        start_d = c1.date_input("Start Date", date(2023, 1, 1))
        end_d = c2.date_input("End Date", date.today())

        st.markdown("**Select Transaction Type:**")
        filter_type = st.radio("Show:", ["All", "Expense", "Income"], horizontal=True, key="date_type_filter")
        st.markdown("---")

        if st.button("🔎 Apply Filter", key="btn_date_filter"):
            raw = db_helper.filter_by_date_range(start_d, end_d)
            df = pd.DataFrame(raw)
            if not df.empty:
                df['type_clean'] = df['transaction_type'].astype(str).str.strip().str.lower()

                if filter_type == "Income":
                    df = df[df['type_clean'].isin(['income', 'credit'])]
                elif filter_type == "Expense":
                    df = df[df['type_clean'].isin(['expense', 'debit'])]

                if not df.empty:
                    df = df.drop(columns=['type_clean'])
                    st.success(f"Found {len(df)} records ({filter_type}).")
                    show_data_with_downloads(df, "date_filtered")
                else:
                    st.warning(f"No {filter_type} records found.")
            else:
                st.warning("No records found.")

    with tab_amt:
        col1, col2 = st.columns(2)
        min_a = col1.number_input("Min Amount (₹)", min_value=0.0, value=0.0)
        max_a = col2.number_input("Max Amount (₹)", min_value=0.0, max_value=1000000000.0, value=100000.0)

        st.markdown("**Select Transaction Type:**")
        filter_type_amt = st.radio("Show:", ["All", "Expense", "Income"], horizontal=True, key="amt_type_filter")
        st.markdown("---")

        if st.button("🔎 Apply Filter", key="btn_amt_filter"):
            raw = db_helper.filter_by_amount_range(min_a, max_a)
            df = pd.DataFrame(raw)
            if not df.empty:
                df['type_clean'] = df['transaction_type'].astype(str).str.strip().str.lower()

                if filter_type_amt == "Income":
                    df = df[df['type_clean'].isin(['income', 'credit'])]
                elif filter_type_amt == "Expense":
                    df = df[df['type_clean'].isin(['expense', 'debit'])]

                if not df.empty:
                    df = df.drop(columns=['type_clean'])
                    st.success(f"Found {len(df)} records ({filter_type_amt}).")
                    show_data_with_downloads(df, "amount_filtered")
                else:
                    st.warning(f"No {filter_type_amt} records found.")
            else:
                st.warning("No records found.")

# ================= 10. DASHBOARD (UNIVERSAL FIX) =================
elif menu == "📊 Dashboard & Charts":
    st.markdown("Analyze your financial growth.")

    tab_d, tab_a, tab_c = st.tabs(["📅 Date Analysis", "💰 Amount Analysis", "⚡ Combined Analysis"])

    # --- TAB 1: DATE ANALYSIS ---
    with tab_d:
        c1, c2 = st.columns(2)
        d_start = c1.date_input("From", date(2023, 1, 1), key="d_start")
        d_end = c2.date_input("To", date.today(), key="d_end")

        st.markdown("**Analyze Type:**")
        dash_type_d = st.radio("Show:", ["All", "Expense", "Income"], horizontal=True, key="dash_type_d")

        if st.button("🚀 Generate Charts", key="btn_dash_d"):
            raw = db_helper.filter_by_date_range(d_start, d_end)
            df = pd.DataFrame(raw)
            if not df.empty:
                df['type_clean'] = df['transaction_type'].astype(str).str.strip().str.lower()

                if dash_type_d == "Income":
                    df = df[df['type_clean'].isin(['income', 'credit'])]
                elif dash_type_d == "Expense":
                    df = df[df['type_clean'].isin(['expense', 'debit'])]

                if not df.empty:
                    generate_charts(df)
                    show_data_with_downloads(df, "dash_date")
                else:
                    st.warning(f"No {dash_type_d} data found in this range.")
            else:
                st.error("No data found.")

    # --- TAB 2: AMOUNT ANALYSIS ---
    with tab_a:
        c1, c2 = st.columns(2)
        a_min = c1.number_input("Min ₹", min_value=0.0, value=0.0, key="a_min")
        a_max = c2.number_input("Max ₹", min_value=0.0, max_value=1000000000.0, value=100000.0, key="a_max")

        st.markdown("**Analyze Type:**")
        dash_type_a = st.radio("Show:", ["All", "Expense", "Income"], horizontal=True, key="dash_type_a")

        if st.button("🚀 Generate Charts", key="btn_dash_a"):
            raw = db_helper.filter_by_amount_range(a_min, a_max)
            df = pd.DataFrame(raw)
            if not df.empty:
                df['type_clean'] = df['transaction_type'].astype(str).str.strip().str.lower()

                if dash_type_a == "Income":
                    df = df[df['type_clean'].isin(['income', 'credit'])]
                elif dash_type_a == "Expense":
                    df = df[df['type_clean'].isin(['expense', 'debit'])]

                if not df.empty:
                    generate_charts(df)
                    show_data_with_downloads(df, "dash_amount")
                else:
                    st.warning(f"No {dash_type_a} data found in this range.")
            else:
                st.error("No data found.")

    # --- TAB 3: COMBINED ANALYSIS ---
    with tab_c:
        c1, c2, c3, c4 = st.columns(4)
        cd_start = c1.date_input("Start", date(2023, 1, 1), key="cd_start")
        cd_end = c2.date_input("End", date.today(), key="cd_end")
        ca_min = c3.number_input("Min ₹", min_value=0.0, value=0.0, key="ca_min")
        ca_max = c4.number_input("Max ₹", min_value=0.0, max_value=1000000000.0, value=100000.0, key="ca_max")

        st.markdown("**Analyze Type:**")
        dash_type_c = st.radio("Show:", ["All", "Expense", "Income"], horizontal=True, key="dash_type_c")

        if st.button("🚀 Generate Combined Charts", key="btn_dash_c"):
            raw = db_helper.filter_by_date_range(cd_start, cd_end)
            df = pd.DataFrame(raw)
            if not df.empty:
                # UPDATE: Changed 'debit_or_credit' to 'amount'
                df['amount'] = pd.to_numeric(df['amount'])
                df = df[(df['amount'] >= ca_min) & (df['amount'] <= ca_max)]

                df['type_clean'] = df['transaction_type'].astype(str).str.strip().str.lower()

                if dash_type_c == "Income":
                    df = df[df['type_clean'].isin(['income', 'credit'])]
                elif dash_type_c == "Expense":
                    df = df[df['type_clean'].isin(['expense', 'debit'])]

                if not df.empty:
                    generate_charts(df)
                    show_data_with_downloads(df, "dash_combined")
                else:
                    st.warning(f"No {dash_type_c} data found matching criteria.")
            else:
                st.warning("No data found in date range.")