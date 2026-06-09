
# ============================================================
#  FinanceIQ — AI-Powered Personal Finance Analytics Dashboard
#  Single-file Streamlit App | app.py
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import os
import io

# ── Page config (MUST be first Streamlit call) ───────────────
st.set_page_config(
    layout="wide",
    page_title="FinanceIQ",
    page_icon="💰",
    initial_sidebar_state="expanded",
)

# ── Colour palette ───────────────────────────────────────────
PALETTE = [
    "#6C63FF", "#00D09C", "#FF6B6B", "#FFD700",
    "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
    "#DDA0DD", "#FF7675",
]
ACCENT   = "#6C63FF"
GREEN    = "#00D09C"
RED      = "#FF6B6B"
GOLD     = "#FFD700"
CARD_BG  = "#1A1D27"
BG       = "#0F1117"

CHART_LAYOUT = dict(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    legend=dict(font=dict(color="white")),
    xaxis=dict(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.1)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.1)"),
)


# ════════════════════════════════════════════════════════════
#  CSS INJECTION
# ════════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}

/* ── App background ── */
.stApp {
    background: #0F1117 !important;
}

/* ── Custom scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #1A1D27; }
::-webkit-scrollbar-thumb { background: #6C63FF; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #4a41d8; }

/* ── Sidebar glassmorphism ── */
[data-testid="stSidebar"] {
    background: rgba(15, 17, 23, 0.92) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(108, 99, 255, 0.2) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* ── Header gradient banner ── */
.header-banner {
    background: linear-gradient(135deg, #1a1d27 0%, #0d0f1a 40%, #1a1040 100%);
    border: 1px solid rgba(108, 99, 255, 0.3);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    animation: fadeInDown 0.6s ease forwards;
}
.header-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(108,99,255,0.15) 0%, transparent 60%),
                radial-gradient(circle at 70% 50%, rgba(0,208,156,0.08) 0%, transparent 60%);
    animation: gradientShift 8s ease-in-out infinite;
}
@keyframes gradientShift {
    0%, 100% { transform: rotate(0deg); }
    50% { transform: rotate(180deg); }
}
.header-title {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6C63FF 0%, #00D09C 50%, #FFD700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
    margin: 0;
    line-height: 1.2;
}
.header-subtitle {
    color: rgba(255,255,255,0.6);
    font-size: 1rem;
    font-weight: 400;
    position: relative;
    z-index: 1;
    margin-top: 0.4rem;
    letter-spacing: 0.05em;
}

/* ── KPI metric cards ── */
.kpi-card {
    background: rgba(26, 29, 39, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    opacity: 0;
    animation: fadeInUp 0.5s ease forwards;
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(108, 99, 255, 0.25);
    border-color: rgba(108, 99, 255, 0.4);
}
.kpi-card:nth-child(1) { animation-delay: 0.0s; }
.kpi-card:nth-child(2) { animation-delay: 0.1s; }
.kpi-card:nth-child(3) { animation-delay: 0.2s; }
.kpi-card:nth-child(4) { animation-delay: 0.3s; }
.kpi-card:nth-child(5) { animation-delay: 0.4s; }

.kpi-icon { font-size: 1.8rem; margin-bottom: 0.4rem; }
.kpi-label {
    color: rgba(255,255,255,0.5);
    font-size: 0.72rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.4rem;
}
.kpi-value {
    font-size: 1.8rem;
    font-weight: 700;
    line-height: 1;
}
.kpi-delta {
    font-size: 0.75rem;
    margin-top: 0.4rem;
    opacity: 0.7;
}

/* ── Section headers ── */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: rgba(255,255,255,0.85);
    border-left: 3px solid #6C63FF;
    padding-left: 0.75rem;
    margin: 1.2rem 0 0.8rem 0;
}

/* ── Chart containers ── */
.chart-container {
    background: rgba(26, 29, 39, 0.6);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1rem;
    animation: fadeIn 0.7s ease forwards;
}

/* ── Tab styling ── */
[data-baseweb="tab-list"] {
    background: rgba(26, 29, 39, 0.8) !important;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(255,255,255,0.06);
    gap: 2px;
}
[data-baseweb="tab"] {
    border-radius: 8px !important;
    color: rgba(255,255,255,0.55) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 0.9rem !important;
    transition: all 0.2s ease !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: linear-gradient(135deg, #6C63FF, #4a41d8) !important;
    color: white !important;
}

/* ── Sidebar elements ── */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stDateInput label {
    color: rgba(255,255,255,0.75) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}

/* ── Filter count pill ── */
.filter-pill {
    background: linear-gradient(135deg, #6C63FF22, #00D09C22);
    border: 1px solid rgba(108, 99, 255, 0.4);
    border-radius: 20px;
    padding: 0.4rem 1rem;
    text-align: center;
    color: #6C63FF;
    font-weight: 600;
    font-size: 0.85rem;
    margin-top: 0.5rem;
}

/* ── Insight cards ── */
.insight-card {
    background: rgba(108, 99, 255, 0.08);
    border: 1px solid rgba(108, 99, 255, 0.25);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 0.5rem 0;
    animation: fadeInLeft 0.5s ease forwards;
}

/* ── Table styling ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
}

/* ── Button styling ── */
.stButton > button {
    background: linear-gradient(135deg, #6C63FF, #4a41d8) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(108, 99, 255, 0.5) !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #00D09C, #00a07a) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ── Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes fadeInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.6; }
}

/* ── No data message ── */
.no-data-msg {
    background: rgba(255, 107, 107, 0.08);
    border: 1px dashed rgba(255, 107, 107, 0.4);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    color: rgba(255,255,255,0.5);
    font-size: 1rem;
    margin: 1rem 0;
}

/* ── Spinner override ── */
[data-testid="stSpinner"] > div {
    border-top-color: #6C63FF !important;
}

/* ── Metric delta ── */
[data-testid="stMetricDelta"] { display: none; }

/* ── Remove default streamlit padding on some elements ── */
.block-container { padding-top: 1rem !important; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  DATA LOADING & CLEANING
# ════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_and_clean(filepath="clean_finance_dataset.xlsx"):
    df = pd.read_excel(filepath)

    # ── Date parsing ─────────────────────────────────────────
    if pd.api.types.is_numeric_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"], origin="1899-12-30", unit="D")
    else:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["date"], inplace=True)

    # ── Category normalisation ────────────────────────────────
    cat_map = {
        "food":          ["food", "foodd"],
        "rent":          ["rent", "rnt"],
        "travel":        ["travel", "traval", "traval", "traval"],
        "health":        ["health", "helth"],
        "education":     ["education", "edu"],
        "entertainment": ["entertainment", "entertain", "entrtnmnt"],
        "utilities":     ["utilities", "utility"],
        "savings":       ["savings", "saving"],
        "investment":    ["investment"],
        "freelance":     ["freelance"],
        "salary":        ["salary"],
        "bonus":         ["bonus"],
    }
    def norm_cat(val):
        v = str(val).strip().lower()
        for clean, variants in cat_map.items():
            if v in variants:
                return clean.capitalize()
        return "Others"
    df["category"] = df["category"].apply(norm_cat)

    # ── Payment mode normalisation ────────────────────────────
    def norm_pay(val):
        v = str(val).strip().lower().replace(" ", "").replace("_", "")
        if v in ("cash", "csh"):
            return "Cash"
        if v in ("card", "crd"):
            return "Card"
        if v in ("upi", "upi", "upi"):
            return "UPI"
        if v in ("banktransfer", "banktransfr"):
            return "Bank Transfer"
        return "Unknown"
    df["payment_mode"] = df["payment_mode"].apply(norm_pay)

    # ── Location normalisation ────────────────────────────────
    loc_map = {
        "Delhi":     ["del", "delhi"],
        "Mumbai":    ["mum", "mumbai"],
        "Bangalore": ["ban", "bangalore"],
        "Hyderabad": ["hyd", "hyderabad"],
        "Chennai":   ["che", "chennai"],
        "Kolkata":   ["kol", "kolkata"],
        "Pune":      ["pun", "pune"],
        "Jaipur":    ["jai", "jaipur"],
        "Lucknow":   ["luc", "lucknow"],
        "Ahmedabad": ["ahm", "ahmedabad"],
    }
    def norm_loc(val):
        v = str(val).strip().lower()
        for city, variants in loc_map.items():
            if v in variants:
                return city
        return "Unknown"
    df["location"] = df["location"].apply(norm_loc)

    # ── Amount cleaning ───────────────────────────────────────
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df[(df["amount"] > 0) & (df["amount"] <= 500_000)].copy()

    # ── Derived columns ───────────────────────────────────────
    df["month"]       = df["date"].dt.to_period("M").astype(str)
    df["year"]        = df["date"].dt.year
    df["quarter"]     = "Q" + df["date"].dt.quarter.astype(str)
    df["day_of_week"] = df["date"].dt.strftime("%a")
    df["is_expense"]  = df["transaction_type"] == "Expense"

    df.sort_values("date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# ════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════
def fmt_inr(val):
    """Format number as Indian Rupee string."""
    if abs(val) >= 1_00_00_000:
        return f"₹{val/1_00_00_000:.1f}Cr"
    elif abs(val) >= 1_00_000:
        return f"₹{val/1_00_000:.1f}L"
    elif abs(val) >= 1_000:
        return f"₹{val/1_000:.1f}K"
    return f"₹{val:,.0f}"


def no_data_msg():
    st.markdown('<div class="no-data-msg">🔍 No data matches the current filters. Adjust your selections to see results.</div>', unsafe_allow_html=True)


def apply_chart_defaults(fig, height=400):
    fig.update_layout(**CHART_LAYOUT, height=height)
    return fig


def kpi_card(icon, label, value, color="#FFFFFF", delta_text=""):
    delta_html = f'<div class="kpi-delta">{delta_text}</div>' if delta_text else ""
    return f"""
<div class="kpi-card">
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-value" style="color:{color}">{value}</div>
  {delta_html}
</div>"""


# ════════════════════════════════════════════════════════════
#  AI INSIGHTS (Claude)
# ════════════════════════════════════════════════════════════
def build_summary_prompt(df: pd.DataFrame) -> str:
    total_tx     = len(df)
    inc_df       = df[df["transaction_type"] == "Income"]
    exp_df       = df[df["transaction_type"] == "Expense"]
    total_income = inc_df["amount"].sum()
    total_exp    = exp_df["amount"].sum()
    net          = total_income - total_exp
    savings_rate = (net / total_income * 100) if total_income > 0 else 0

    top_cats     = exp_df.groupby("category")["amount"].sum().sort_values(ascending=False).head(5).to_dict()
    top_cities   = df.groupby("location")["amount"].sum().sort_values(ascending=False).head(5).to_dict()
    pay_pref     = df.groupby("payment_mode")["amount"].sum().sort_values(ascending=False).to_dict()
    monthly      = df.groupby(["month", "transaction_type"])["amount"].sum().unstack(fill_value=0).tail(6).to_dict()

    prompt = f"""You are FinanceIQ, an expert AI financial analyst. Analyse the following personal finance dataset summary and provide a detailed, actionable report.

## Dataset Summary
- **Total Transactions**: {total_tx:,}
- **Total Income**: ₹{total_income:,.0f}
- **Total Expenses**: ₹{total_exp:,.0f}
- **Net Balance**: ₹{net:,.0f}
- **Savings Rate**: {savings_rate:.1f}%

## Top Expense Categories
{', '.join([f"{k}: ₹{v:,.0f}" for k,v in top_cats.items()])}

## City-wise Spending
{', '.join([f"{k}: ₹{v:,.0f}" for k,v in top_cities.items()])}

## Payment Method Preferences
{', '.join([f"{k}: ₹{v:,.0f}" for k,v in pay_pref.items()])}

## Recent Monthly Trend (last 6 months)
{monthly}

---
Please respond with a well-structured markdown report containing exactly these sections:
1. ### 🔑 Key Insights (5-7 bullet points of most important findings)
2. ### ⚠️ Anomalies Detected (unusual patterns, spikes, or concerns)
3. ### 💡 Spending Recommendations (5 actionable recommendations)
4. ### 📊 Financial Health Score: X/10 (with detailed justification)

Keep the tone professional but friendly. Format numbers in Indian notation (Lakhs/Crores where applicable).
"""
    return prompt


def get_api_key() -> str:
    """Read API key from st.secrets (Streamlit Cloud) or environment variable."""
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        return os.environ.get("ANTHROPIC_API_KEY", "")


@st.cache_data(ttl=300, show_spinner=False)
def get_ai_insights(prompt_key: str, prompt: str) -> str:
    try:
        import anthropic
        api_key = get_api_key()
        if not api_key:
            return "⚠️ **API key not found.**\n\nTo enable AI Insights:\n- **Locally**: set `ANTHROPIC_API_KEY` environment variable\n- **Streamlit Cloud**: add `ANTHROPIC_API_KEY = \"sk-ant-...\"` in App Settings → Secrets"
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text
    except ImportError:
        return "⚠️ The `anthropic` package is not installed. Run `pip install anthropic` to enable AI Insights."
    except Exception as e:
        return f"⚠️ Could not generate insights: {str(e)}"


@st.cache_data(ttl=300, show_spinner=False)
def ask_claude(question: str, context: str) -> str:
    try:
        import anthropic
        api_key = get_api_key()
        if not api_key:
            return "⚠️ API key not set. Add `ANTHROPIC_API_KEY` to your environment or Streamlit secrets."
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=800,
            messages=[{
                "role": "user",
                "content": f"You are FinanceIQ assistant. Here is the financial dataset context:\n\n{context}\n\nUser question: {question}\n\nProvide a concise, helpful answer."
            }],
        )
        return msg.content[0].text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# ════════════════════════════════════════════════════════════
#  TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════
def render_overview(df: pd.DataFrame):
    if df.empty:
        no_data_msg(); return

    inc_df = df[df["transaction_type"] == "Income"]
    exp_df = df[df["transaction_type"] == "Expense"]
    total_income = inc_df["amount"].sum()
    total_exp    = exp_df["amount"].sum()
    net          = total_income - total_exp
    avg_tx       = df["amount"].mean()

    # ── KPI Cards ────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    cards = [
        (c1, "🔢", "Total Transactions", f"{len(df):,}", "#FFFFFF"),
        (c2, "💚", "Total Income",       fmt_inr(total_income), GREEN),
        (c3, "❤️",  "Total Expenses",    fmt_inr(total_exp),    RED),
        (c4, "⚖️",  "Net Balance",       fmt_inr(net),          GREEN if net >= 0 else RED),
        (c5, "📐", "Avg Transaction",   fmt_inr(avg_tx),       GOLD),
    ]
    for col, icon, label, value, color in cards:
        col.markdown(kpi_card(icon, label, value, color), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2 ─────────────────────────────────────────────────
    col_l, col_r = st.columns([6, 4])

    with col_l:
        st.markdown('<div class="section-header">📅 Monthly Income vs Expenses</div>', unsafe_allow_html=True)
        monthly = df.groupby(["month", "transaction_type"])["amount"].sum().reset_index()
        if not monthly.empty:
            fig = px.bar(
                monthly, x="month", y="amount", color="transaction_type",
                barmode="group",
                color_discrete_map={"Income": GREEN, "Expense": RED},
                labels={"amount": "Amount (₹)", "month": "Month", "transaction_type": "Type"},
            )
            fig.update_traces(hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>")
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-header">🍩 Transaction Split</div>', unsafe_allow_html=True)
        type_counts = df.groupby("transaction_type")["amount"].sum().reset_index()
        if not type_counts.empty:
            fig = go.Figure(go.Pie(
                labels=type_counts["transaction_type"],
                values=type_counts["amount"],
                hole=0.62,
                marker_colors=[GREEN, RED],
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>",
            ))
            fig.add_annotation(
                text=f"Net<br>{fmt_inr(net)}",
                font=dict(size=14, color="white", family="Inter"),
                showarrow=False,
            )
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    # ── Row 3 ─────────────────────────────────────────────────
    col_l2, col_r2 = st.columns(2)

    with col_l2:
        st.markdown('<div class="section-header">📦 Expense by Category</div>', unsafe_allow_html=True)
        cat_exp = exp_df.groupby("category")["amount"].sum().sort_values().reset_index()
        if not cat_exp.empty:
            fig = px.bar(
                cat_exp, x="amount", y="category", orientation="h",
                color="amount", color_continuous_scale=["#6C63FF", "#00D09C"],
                labels={"amount": "Amount (₹)", "category": ""},
            )
            fig.update_traces(
                text=[fmt_inr(v) for v in cat_exp["amount"]],
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
            )
            fig.update_layout(coloraxis_showscale=False)
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    with col_r2:
        st.markdown('<div class="section-header">💰 Income Sources</div>', unsafe_allow_html=True)
        inc_cat = inc_df.groupby("category")["amount"].sum().reset_index()
        if not inc_cat.empty:
            fig = px.pie(
                inc_cat, names="category", values="amount",
                color_discrete_sequence=PALETTE,
                hole=0.3,
            )
            fig.update_traces(hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>")
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No income data available.")

    # ── Row 4 ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">📉 Daily Spending Trend</div>', unsafe_allow_html=True)
    daily = exp_df.groupby("date")["amount"].sum().reset_index()
    daily = daily.sort_values("date")
    if not daily.empty:
        daily["ma7"] = daily["amount"].rolling(7, min_periods=1).mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily["date"], y=daily["amount"],
            fill="tozeroy",
            fillcolor="rgba(108,99,255,0.15)",
            line=dict(color=ACCENT, width=1.5),
            name="Daily Expense",
            hovertemplate="<b>%{x|%d %b %Y}</b><br>₹%{y:,.0f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=daily["date"], y=daily["ma7"],
            line=dict(color=GREEN, width=2.5, dash="dot"),
            name="7-day Moving Avg",
            hovertemplate="<b>%{x|%d %b %Y}</b><br>MA7: ₹%{y:,.0f}<extra></extra>",
        ))
        fig.update_layout(
            xaxis=dict(rangeslider=dict(visible=True, thickness=0.06), type="date"),
        )
        fig = apply_chart_defaults(fig, 500)
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════
#  TAB 2 — TRENDS & TIME ANALYSIS
# ════════════════════════════════════════════════════════════
def render_trends(df: pd.DataFrame):
    if df.empty:
        no_data_msg(); return

    exp_df = df[df["transaction_type"] == "Expense"]

    # ── Row 1: Monthly Heatmap ────────────────────────────────
    st.markdown('<div class="section-header">🗓️ Monthly Spending Heatmap</div>', unsafe_allow_html=True)
    monthly_exp = exp_df.groupby("month")["amount"].sum().reset_index()
    monthly_exp["month_dt"] = pd.to_datetime(monthly_exp["month"])
    monthly_exp["mon_label"] = monthly_exp["month_dt"].dt.strftime("%b %Y")
    monthly_exp = monthly_exp.sort_values("month_dt")
    if not monthly_exp.empty:
        # Build pivot: year × month_abbr
        monthly_exp["yr"]  = monthly_exp["month_dt"].dt.year
        monthly_exp["mon"] = monthly_exp["month_dt"].dt.strftime("%b")
        pivot = monthly_exp.pivot_table(index="yr", columns="mon", values="amount", aggfunc="sum")
        month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        pivot = pivot.reindex(columns=[m for m in month_order if m in pivot.columns])
        fig = px.imshow(
            pivot,
            color_continuous_scale="Viridis",
            labels=dict(color="Spend (₹)"),
            aspect="auto",
        )
        fig.update_traces(hovertemplate="Year: %{y}<br>Month: %{x}<br>₹%{z:,.0f}<extra></extra>")
        fig = apply_chart_defaults(fig, 350)
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2 ─────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">📊 Quarter-wise Income vs Expense</div>', unsafe_allow_html=True)
        qtr = df.groupby(["year","quarter","transaction_type"])["amount"].sum().reset_index()
        qtr["period"] = qtr["year"].astype(str) + " " + qtr["quarter"]
        if not qtr.empty:
            fig = px.bar(
                qtr, x="period", y="amount", color="transaction_type",
                barmode="group",
                color_discrete_map={"Income": GREEN, "Expense": RED},
                labels={"amount": "Amount (₹)", "period": "Quarter"},
            )
            fig.update_traces(hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>")
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">📅 Year-over-Year Comparison</div>', unsafe_allow_html=True)
        yoy = df.groupby(["year","transaction_type"])["amount"].sum().reset_index()
        if not yoy.empty:
            fig = px.line(
                yoy, x="year", y="amount", color="transaction_type",
                markers=True,
                color_discrete_map={"Income": GREEN, "Expense": RED},
                labels={"amount": "Amount (₹)", "year": "Year"},
            )
            fig.update_traces(hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>")
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    # ── Row 3 ─────────────────────────────────────────────────
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="section-header">🕸️ Day of Week Spending Pattern</div>', unsafe_allow_html=True)
        dow_order = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        dow = exp_df.groupby("day_of_week")["amount"].mean().reindex(dow_order).fillna(0).reset_index()
        if not dow.empty:
            fig = go.Figure(go.Scatterpolar(
                r=dow["amount"],
                theta=dow["day_of_week"],
                fill="toself",
                fillcolor="rgba(108,99,255,0.25)",
                line=dict(color=ACCENT, width=2),
                hovertemplate="<b>%{theta}</b><br>Avg: ₹%{r:,.0f}<extra></extra>",
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, gridcolor="rgba(255,255,255,0.1)", color="white"),
                    angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", color="white"),
                ),
            )
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.markdown('<div class="section-header">💳 Payment Mode Over Time</div>', unsafe_allow_html=True)
        pm_time = df.groupby(["month","payment_mode"])["amount"].sum().reset_index()
        pm_time = pm_time.sort_values("month")
        if not pm_time.empty:
            fig = px.area(
                pm_time, x="month", y="amount", color="payment_mode",
                color_discrete_sequence=PALETTE,
                labels={"amount": "Amount (₹)", "month": "Month", "payment_mode": "Mode"},
            )
            fig.update_traces(hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>")
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    # ── Row 4: Savings Rate ───────────────────────────────────
    st.markdown('<div class="section-header">💾 Rolling Monthly Savings Rate (%)</div>', unsafe_allow_html=True)
    monthly_inc = df[df["transaction_type"]=="Income"].groupby("month")["amount"].sum()
    monthly_exs = df[df["transaction_type"]=="Expense"].groupby("month")["amount"].sum()
    sv_rate = ((monthly_inc - monthly_exs) / monthly_inc * 100).dropna().reset_index()
    sv_rate.columns = ["month","savings_rate"]
    sv_rate = sv_rate.sort_values("month")
    if not sv_rate.empty:
        sv_rate["color"] = sv_rate["savings_rate"].apply(lambda x: GREEN if x >= 0 else RED)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sv_rate["month"], y=sv_rate["savings_rate"],
            fill="tozeroy",
            fillcolor="rgba(0,208,156,0.15)",
            line=dict(color=GREEN, width=2.5),
            hovertemplate="<b>%{x}</b><br>Savings Rate: %{y:.1f}%<extra></extra>",
            name="Savings Rate",
        ))
        fig.add_hline(y=0, line_dash="dot", line_color=RED, annotation_text="Break-even", annotation_font_color=RED)
        fig.update_layout(yaxis_title="Savings Rate (%)", xaxis_title="Month")
        fig = apply_chart_defaults(fig, 400)
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════
#  TAB 3 — LOCATION INTELLIGENCE
# ════════════════════════════════════════════════════════════
def render_location(df: pd.DataFrame):
    if df.empty:
        no_data_msg(); return

    exp_df = df[df["transaction_type"]=="Expense"]

    # ── Row 1 ─────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">🏙️ City-wise Total Spending</div>', unsafe_allow_html=True)
        city_spend = exp_df.groupby("location")["amount"].sum().sort_values().reset_index()
        if not city_spend.empty:
            fig = px.bar(
                city_spend, x="amount", y="location", orientation="h",
                color="amount", color_continuous_scale=["#6C63FF","#00D09C"],
                labels={"amount": "Total Spend (₹)", "location": ""},
            )
            fig.update_traces(
                text=[fmt_inr(v) for v in city_spend["amount"]],
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
            )
            fig.update_layout(coloraxis_showscale=False)
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">🗺️ City-wise Transaction Count (Treemap)</div>', unsafe_allow_html=True)
        city_cnt = df.groupby("location").size().reset_index(name="count")
        if not city_cnt.empty:
            fig = px.treemap(
                city_cnt, path=["location"], values="count",
                color="count", color_continuous_scale="Viridis",
                hover_data={"count": True},
            )
            fig.update_traces(hovertemplate="<b>%{label}</b><br>Transactions: %{value:,}<extra></extra>")
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    # ── Row 2: City × Category Heatmap ───────────────────────
    st.markdown('<div class="section-header">🔥 City × Category Spending Heatmap</div>', unsafe_allow_html=True)
    cc = exp_df.groupby(["location","category"])["amount"].sum().reset_index()
    if not cc.empty:
        pivot = cc.pivot_table(index="location", columns="category", values="amount", fill_value=0)
        fig = px.imshow(
            pivot,
            color_continuous_scale="Viridis",
            labels=dict(color="Spend (₹)"),
            aspect="auto",
        )
        fig.update_traces(hovertemplate="City: %{y}<br>Category: %{x}<br>₹%{z:,.0f}<extra></extra>")
        fig = apply_chart_defaults(fig, 450)
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 3 ─────────────────────────────────────────────────
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="section-header">🏆 Top 5 Cities by Avg Transaction</div>', unsafe_allow_html=True)
        avg_city = df.groupby("location")["amount"].mean().sort_values(ascending=False).head(5).reset_index()
        if not avg_city.empty:
            fig = px.bar(
                avg_city, x="location", y="amount",
                color="amount", color_continuous_scale=["#6C63FF","#FFD700"],
                labels={"amount": "Avg Amount (₹)", "location": "City"},
            )
            fig.update_traces(
                text=[fmt_inr(v) for v in avg_city["amount"]],
                textposition="outside",
                hovertemplate="<b>%{x}</b><br>Avg: ₹%{y:,.0f}<extra></extra>",
            )
            fig.update_layout(coloraxis_showscale=False)
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.markdown('<div class="section-header">⚖️ City-wise Income vs Expense</div>', unsafe_allow_html=True)
        city_ie = df.groupby(["location","transaction_type"])["amount"].sum().reset_index()
        if not city_ie.empty:
            fig = px.bar(
                city_ie, x="location", y="amount", color="transaction_type",
                barmode="group",
                color_discrete_map={"Income": GREEN, "Expense": RED},
                labels={"amount": "Amount (₹)", "location": "City"},
            )
            fig.update_traces(hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>")
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════
#  TAB 4 — PAYMENT ANALYSIS
# ════════════════════════════════════════════════════════════
def render_payment(df: pd.DataFrame):
    if df.empty:
        no_data_msg(); return

    # ── Row 1 ─────────────────────────────────────────────────
    c1, c2, c3 = st.columns([4, 3, 3])
    with c1:
        st.markdown('<div class="section-header">🍩 Payment Mode Distribution</div>', unsafe_allow_html=True)
        pm_amt = df.groupby("payment_mode")["amount"].sum().reset_index()
        if not pm_amt.empty:
            fig = go.Figure(go.Pie(
                labels=pm_amt["payment_mode"], values=pm_amt["amount"],
                hole=0.58, marker_colors=PALETTE,
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>",
            ))
            fig = apply_chart_defaults(fig, 350)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">🔢 Transaction Count</div>', unsafe_allow_html=True)
        pm_cnt = df.groupby("payment_mode").size().reset_index(name="count")
        if not pm_cnt.empty:
            fig = px.bar(
                pm_cnt, x="payment_mode", y="count",
                color="payment_mode", color_discrete_sequence=PALETTE,
                labels={"count": "Transactions", "payment_mode": ""},
            )
            fig.update_layout(showlegend=False)
            fig.update_traces(hovertemplate="<b>%{x}</b><br>%{y:,} transactions<extra></extra>")
            fig = apply_chart_defaults(fig, 350)
            st.plotly_chart(fig, use_container_width=True)

    with c3:
        st.markdown('<div class="section-header">💵 Avg Amount per Mode</div>', unsafe_allow_html=True)
        pm_avg = df.groupby("payment_mode")["amount"].mean().reset_index()
        if not pm_avg.empty:
            fig = px.bar(
                pm_avg, x="payment_mode", y="amount",
                color="payment_mode", color_discrete_sequence=PALETTE,
                labels={"amount": "Avg Amount (₹)", "payment_mode": ""},
            )
            fig.update_layout(showlegend=False)
            fig.update_traces(
                text=[fmt_inr(v) for v in pm_avg["amount"]],
                textposition="outside",
                hovertemplate="<b>%{x}</b><br>Avg: ₹%{y:,.0f}<extra></extra>",
            )
            fig = apply_chart_defaults(fig, 350)
            st.plotly_chart(fig, use_container_width=True)

    # ── Row 2 ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">📈 Payment Mode Trend Over Time</div>', unsafe_allow_html=True)
    pm_trend = df.groupby(["month","payment_mode"])["amount"].sum().reset_index().sort_values("month")
    if not pm_trend.empty:
        fig = px.area(
            pm_trend, x="month", y="amount", color="payment_mode",
            color_discrete_sequence=PALETTE,
            labels={"amount": "Amount (₹)", "month": "Month", "payment_mode": "Mode"},
        )
        fig.update_traces(hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>")
        fig = apply_chart_defaults(fig, 450)
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 3 ─────────────────────────────────────────────────
    c4, c5 = st.columns(2)
    with c4:
        st.markdown('<div class="section-header">🔀 Payment Mode × Category</div>', unsafe_allow_html=True)
        pm_cat = df.groupby(["payment_mode","category"])["amount"].sum().reset_index()
        if not pm_cat.empty:
            fig = px.bar(
                pm_cat, x="category", y="amount", color="payment_mode",
                barmode="group",
                color_discrete_sequence=PALETTE,
                labels={"amount": "Amount (₹)", "category": "Category", "payment_mode": "Mode"},
            )
            fig.update_traces(hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>")
            fig.update_layout(xaxis_tickangle=-35)
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    with c5:
        st.markdown('<div class="section-header">💡 Cash vs Digital Ratio Over Time</div>', unsafe_allow_html=True)
        df2 = df.copy()
        df2["mode_type"] = df2["payment_mode"].apply(lambda x: "Cash" if x == "Cash" else "Digital")
        cd_time = df2.groupby(["month","mode_type"])["amount"].sum().unstack(fill_value=0).reset_index()
        cd_time = cd_time.sort_values("month")
        if not cd_time.empty and "Cash" in cd_time.columns and "Digital" in cd_time.columns:
            cd_time["total"] = cd_time["Cash"] + cd_time["Digital"]
            cd_time["cash_pct"]    = cd_time["Cash"] / cd_time["total"] * 100
            cd_time["digital_pct"] = cd_time["Digital"] / cd_time["total"] * 100
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=cd_time["month"], y=cd_time["digital_pct"],
                fill="tozeroy", fillcolor="rgba(0,208,156,0.2)",
                line=dict(color=GREEN, width=2),
                name="Digital %",
                hovertemplate="<b>%{x}</b><br>Digital: %{y:.1f}%<extra></extra>",
            ))
            fig.add_trace(go.Scatter(
                x=cd_time["month"], y=cd_time["cash_pct"],
                fill="tozeroy", fillcolor="rgba(255,107,107,0.15)",
                line=dict(color=RED, width=2),
                name="Cash %",
                hovertemplate="<b>%{x}</b><br>Cash: %{y:.1f}%<extra></extra>",
            ))
            fig.update_layout(yaxis_title="% of Total Amount")
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient data for Cash vs Digital breakdown.")


# ════════════════════════════════════════════════════════════
#  TAB 5 — USER ANALYTICS
# ════════════════════════════════════════════════════════════
def render_users(df: pd.DataFrame):
    if df.empty:
        no_data_msg(); return

    exp_df = df[df["transaction_type"]=="Expense"]
    inc_df = df[df["transaction_type"]=="Income"]

    # ── Row 1 ─────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">🏆 Top 10 Users by Total Spending</div>', unsafe_allow_html=True)
        top_spend = exp_df.groupby("user_id")["amount"].sum().sort_values(ascending=True).tail(10).reset_index()
        if not top_spend.empty:
            fig = px.bar(
                top_spend, x="amount", y="user_id", orientation="h",
                color="amount", color_continuous_scale=["#6C63FF","#FF6B6B"],
                labels={"amount": "Total Spend (₹)", "user_id": "User"},
            )
            fig.update_traces(
                text=[fmt_inr(v) for v in top_spend["amount"]],
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
            )
            fig.update_layout(coloraxis_showscale=False)
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">📊 Top 10 Users by Transaction Count</div>', unsafe_allow_html=True)
        top_cnt = df.groupby("user_id").size().sort_values(ascending=False).head(10).reset_index(name="count")
        if not top_cnt.empty:
            fig = px.bar(
                top_cnt, x="user_id", y="count",
                color="count", color_continuous_scale=["#6C63FF","#00D09C"],
                labels={"count": "Transactions", "user_id": "User"},
            )
            fig.update_traces(hovertemplate="<b>%{x}</b><br>%{y:,} transactions<extra></extra>")
            fig.update_layout(coloraxis_showscale=False)
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    # ── Row 2: Box Plot ───────────────────────────────────────
    st.markdown('<div class="section-header">📦 User Spending Distribution by Category</div>', unsafe_allow_html=True)
    if not exp_df.empty:
        fig = px.box(
            exp_df, x="category", y="amount",
            color="category", color_discrete_sequence=PALETTE,
            labels={"amount": "Amount (₹)", "category": "Category"},
        )
        fig.update_traces(hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>")
        fig.update_layout(showlegend=False, xaxis_tickangle=-30)
        fig = apply_chart_defaults(fig, 450)
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 3 ─────────────────────────────────────────────────
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="section-header">🔵 Income vs Expense Scatter</div>', unsafe_allow_html=True)
        user_inc = inc_df.groupby("user_id")["amount"].sum()
        user_exp = exp_df.groupby("user_id")["amount"].sum()
        user_cnt = df.groupby("user_id").size()
        scatter_df = pd.DataFrame({"income": user_inc, "expense": user_exp, "count": user_cnt}).dropna().reset_index()
        scatter_df["net"] = scatter_df["income"] - scatter_df["expense"]
        scatter_df["color"] = scatter_df["net"].apply(lambda x: GREEN if x >= 0 else RED)
        if not scatter_df.empty:
            fig = px.scatter(
                scatter_df, x="income", y="expense", size="count",
                color="net", color_continuous_scale=["#FF6B6B","#00D09C"],
                hover_name="user_id",
                labels={"income": "Total Income (₹)", "expense": "Total Expense (₹)", "net": "Net (₹)"},
                size_max=30,
            )
            fig.add_shape(type="line", x0=0, y0=0,
                          x1=scatter_df["income"].max(), y1=scatter_df["income"].max(),
                          line=dict(dash="dot", color="rgba(255,255,255,0.3)"))
            fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Income: ₹%{x:,.0f}<br>Expense: ₹%{y:,.0f}<extra></extra>")
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.markdown('<div class="section-header">💾 Top 10 Users by Savings Rate</div>', unsafe_allow_html=True)
        sv = pd.DataFrame({"income": user_inc, "expense": user_exp}).dropna()
        sv["savings_rate"] = (sv["income"] - sv["expense"]) / sv["income"] * 100
        sv_top = sv.sort_values("savings_rate", ascending=False).head(10).reset_index()
        if not sv_top.empty:
            sv_top["color"] = sv_top["savings_rate"].apply(lambda x: GREEN if x >= 0 else RED)
            fig = px.bar(
                sv_top, x="user_id", y="savings_rate",
                color="savings_rate", color_continuous_scale=["#FF6B6B","#00D09C"],
                labels={"savings_rate": "Savings Rate (%)", "user_id": "User"},
            )
            fig.add_hline(y=0, line_dash="dot", line_color="white", opacity=0.4)
            fig.update_traces(hovertemplate="<b>%{x}</b><br>Savings Rate: %{y:.1f}%<extra></extra>")
            fig.update_layout(coloraxis_showscale=False)
            fig = apply_chart_defaults(fig, 400)
            st.plotly_chart(fig, use_container_width=True)

    # ── Row 4: Single User Deep Dive ─────────────────────────
    st.markdown('<div class="section-header">🔎 Single User Deep Dive</div>', unsafe_allow_html=True)
    all_users = sorted(df["user_id"].unique().tolist())
    sel_user = st.selectbox("Select User:", all_users, key="deep_dive_user")
    u_df = df[df["user_id"] == sel_user]
    if u_df.empty:
        st.info("No data for this user."); return

    ua, ub, uc, ud = st.columns(4)
    u_inc = u_df[u_df["transaction_type"]=="Income"]["amount"].sum()
    u_exp = u_df[u_df["transaction_type"]=="Expense"]["amount"].sum()
    u_net = u_inc - u_exp
    u_sr  = (u_net / u_inc * 100) if u_inc > 0 else 0
    ua.markdown(kpi_card("📊","Transactions", f"{len(u_df):,}", "#FFFFFF"), unsafe_allow_html=True)
    ub.markdown(kpi_card("💚","Income", fmt_inr(u_inc), GREEN), unsafe_allow_html=True)
    uc.markdown(kpi_card("❤️","Expenses", fmt_inr(u_exp), RED), unsafe_allow_html=True)
    ud.markdown(kpi_card("💾","Savings Rate", f"{u_sr:.1f}%", GREEN if u_sr>=0 else RED), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    with d1:
        u_monthly = u_df.groupby(["month","transaction_type"])["amount"].sum().reset_index()
        fig = px.line(u_monthly, x="month", y="amount", color="transaction_type", markers=True,
                      color_discrete_map={"Income": GREEN, "Expense": RED},
                      title=f"Monthly Trend — {sel_user}")
        fig.update_traces(hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>")
        fig = apply_chart_defaults(fig, 320)
        st.plotly_chart(fig, use_container_width=True)

    with d2:
        u_cat = u_df[u_df["transaction_type"]=="Expense"].groupby("category")["amount"].sum().reset_index()
        fig = px.pie(u_cat, names="category", values="amount", hole=0.45,
                     color_discrete_sequence=PALETTE, title="Expense Categories")
        fig.update_traces(hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>")
        fig = apply_chart_defaults(fig, 320)
        st.plotly_chart(fig, use_container_width=True)

    with d3:
        u_pm = u_df.groupby("payment_mode")["amount"].sum().reset_index()
        fig = px.pie(u_pm, names="payment_mode", values="amount", hole=0.45,
                     color_discrete_sequence=PALETTE[::-1], title="Payment Modes")
        fig.update_traces(hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>")
        fig = apply_chart_defaults(fig, 320)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">📋 Raw Transactions</div>', unsafe_allow_html=True)
    cols_show = ["transaction_id","date","transaction_type","category","amount","payment_mode","location","notes"]
    st.dataframe(
        u_df[cols_show].sort_values("date", ascending=False),
        use_container_width=True, height=300,
    )


# ════════════════════════════════════════════════════════════
#  TAB 6 — TRANSACTION EXPLORER
# ════════════════════════════════════════════════════════════
def render_explorer(df: pd.DataFrame):
    if df.empty:
        no_data_msg(); return

    search_term = st.text_input("🔍 Search by notes keyword:", placeholder="e.g. restaurant, electricity, amazon...")
    expl_df = df.copy()
    if search_term.strip():
        expl_df = expl_df[expl_df["notes"].astype(str).str.contains(search_term, case=False, na=False)]

    st.markdown(f"**Showing {len(expl_df):,} transactions**", unsafe_allow_html=True)

    # Styled dataframe
    display_cols = ["transaction_id","date","user_id","transaction_type","category","amount","payment_mode","location","notes"]
    display_df = expl_df[display_cols].copy()

    def color_amount(val, tx_type):
        return GREEN if tx_type == "Income" else RED

    styled = display_df.style.apply(
        lambda row: [
            f"color: {GREEN if row['transaction_type']=='Income' else RED}" if col == "amount" else ""
            for col in display_df.columns
        ], axis=1
    )
    st.dataframe(styled, use_container_width=True, height=450)

    # ── Download ──────────────────────────────────────────────
    csv_buf = io.StringIO()
    expl_df.to_csv(csv_buf, index=False)
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_buf.getvalue(),
        file_name="financeiq_filtered_data.csv",
        mime="text/csv",
    )

    # ── Summary Stats ─────────────────────────────────────────
    st.markdown('<div class="section-header">📐 Amount Statistics</div>', unsafe_allow_html=True)
    amt_stats = expl_df["amount"].describe()
    s1, s2, s3, s4, s5 = st.columns(5)
    stat_cards = [
        (s1, "🔽", "Min",    fmt_inr(amt_stats["min"]),    ACCENT),
        (s2, "🔼", "Max",    fmt_inr(amt_stats["max"]),    GOLD),
        (s3, "➗", "Mean",   fmt_inr(amt_stats["mean"]),   "#45B7D1"),
        (s4, "⚖️", "Median", fmt_inr(expl_df["amount"].median()), GREEN),
        (s5, "📏", "Std Dev",fmt_inr(amt_stats["std"]),   "#DDA0DD"),
    ]
    for col, icon, label, val, color in stat_cards:
        col.markdown(kpi_card(icon, label, val, color), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  TAB 7 — AI INSIGHTS
# ════════════════════════════════════════════════════════════
def render_ai_insights(df: pd.DataFrame):
    st.markdown("""
<div class="insight-card" style="background: linear-gradient(135deg, rgba(108,99,255,0.12), rgba(0,208,156,0.08)); border-color: rgba(108,99,255,0.4);">
  <h3 style="margin:0; color:#6C63FF;">🤖 FinanceIQ AI Analyst</h3>
  <p style="margin:0.4rem 0 0; color:rgba(255,255,255,0.6); font-size:0.9rem;">
    Powered by Claude Sonnet · Provides personalised financial insights from your data
  </p>
</div>""", unsafe_allow_html=True)

    if df.empty:
        st.warning("No data available for AI analysis. Adjust your filters."); return

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🔮 Generate AI Insights", use_container_width=True):
            st.session_state["gen_insights"] = True
            st.session_state["insights_key"] = str(hash(str(df.shape) + str(df["amount"].sum())))

    with col2:
        if st.button("🗑️ Clear Insights", use_container_width=True):
            st.session_state.pop("ai_insights_text", None)
            st.session_state.pop("gen_insights", None)

    if st.session_state.get("gen_insights", False):
        key = st.session_state.get("insights_key", "default")
        if "ai_insights_text" not in st.session_state:
            with st.spinner("🧠 Claude is analysing your financial data..."):
                prompt = build_summary_prompt(df)
                result = get_ai_insights(key, prompt)
                st.session_state["ai_insights_text"] = result

        if "ai_insights_text" in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state["ai_insights_text"])

    # ── Custom Q&A ────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-header">💬 Ask About Your Finances</div>', unsafe_allow_html=True)
    user_q = st.text_area("Ask anything about your financial data:", placeholder="e.g. Which category am I overspending on? How can I improve my savings?", height=100)

    if st.button("🚀 Ask AI", use_container_width=False):
        if user_q.strip():
            ctx = f"""Dataset summary: {len(df):,} transactions | Income: ₹{df[df['transaction_type']=='Income']['amount'].sum():,.0f} | Expense: ₹{df[df['transaction_type']=='Expense']['amount'].sum():,.0f} | Top categories: {df[df['transaction_type']=='Expense'].groupby('category')['amount'].sum().sort_values(ascending=False).head(3).to_dict()} | Date range: {df['date'].min().date()} to {df['date'].max().date()}"""
            with st.spinner("💭 Thinking..."):
                answer = ask_claude(user_q, ctx)
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown(answer)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter a question first.")


# ════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════
def render_sidebar(df: pd.DataFrame):
    st.sidebar.markdown("""
<div style="text-align:center; padding: 0.5rem 0 1rem;">
  <div style="font-size:2rem;">💰</div>
  <div style="font-size:1.1rem; font-weight:700; color:#6C63FF;">FinanceIQ</div>
  <div style="font-size:0.72rem; color:rgba(255,255,255,0.4); margin-top:0.2rem;">Dashboard Controls</div>
</div>
<hr style="border-color:rgba(255,255,255,0.08); margin-bottom:1rem;">
""", unsafe_allow_html=True)

    st.sidebar.markdown("**🎛️ Filters**")

    # ── Date Range ────────────────────────────────────────────
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # ── Defaults for reset ────────────────────────────────────
    all_types    = ["Expense", "Income"]
    all_cats     = sorted(df["category"].unique().tolist())
    all_locs     = sorted(df["location"].unique().tolist())
    all_modes    = sorted(df["payment_mode"].unique().tolist())
    all_users    = sorted(df["user_id"].unique().tolist())
    amt_min      = int(df["amount"].min())
    amt_max      = int(df["amount"].max())

    if "reset" not in st.session_state:
        st.session_state["reset"] = False

    reset = st.session_state.get("reset", False)

    sel_types = st.sidebar.multiselect("💸 Transaction Type", all_types, default=all_types, key="f_types")
    sel_cats  = st.sidebar.multiselect("📦 Category",         all_cats,  default=all_cats,  key="f_cats")
    sel_locs  = st.sidebar.multiselect("📍 Location",         all_locs,  default=all_locs,  key="f_locs")
    sel_modes = st.sidebar.multiselect("💳 Payment Mode",     all_modes, default=all_modes, key="f_modes")
    sel_users = st.sidebar.multiselect("👤 User",             all_users, default=all_users, key="f_users")
    amt_range = st.sidebar.slider("💰 Amount Range (₹)", amt_min, amt_max, (amt_min, amt_max), key="f_amount")

    if st.sidebar.button("🔄 Reset Filters"):
        for key in ["f_types","f_cats","f_locs","f_modes","f_users","f_amount"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    # ── Apply filters ─────────────────────────────────────────
    fdf = df.copy()

    if len(date_range) == 2:
        start_d, end_d = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        fdf = fdf[(fdf["date"] >= start_d) & (fdf["date"] <= end_d)]

    if sel_types:
        fdf = fdf[fdf["transaction_type"].isin(sel_types)]
    if sel_cats:
        fdf = fdf[fdf["category"].isin(sel_cats)]
    if sel_locs:
        fdf = fdf[fdf["location"].isin(sel_locs)]
    if sel_modes:
        fdf = fdf[fdf["payment_mode"].isin(sel_modes)]
    if sel_users:
        fdf = fdf[fdf["user_id"].isin(sel_users)]

    fdf = fdf[(fdf["amount"] >= amt_range[0]) & (fdf["amount"] <= amt_range[1])]

    # ── Transaction counter pill ──────────────────────────────
    pct = (len(fdf) / len(df) * 100) if len(df) > 0 else 0
    st.sidebar.markdown(f"""
<div class="filter-pill">
  📊 {len(fdf):,} transactions selected<br>
  <span style="font-size:0.7rem; opacity:0.7;">({pct:.1f}% of total)</span>
</div>""", unsafe_allow_html=True)

    return fdf


# ════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════
def main():
    inject_css()

    # ── Header ────────────────────────────────────────────────
    st.markdown("""
<div class="header-banner">
  <h1 class="header-title">💰 FinanceIQ — Personal Finance Analytics</h1>
  <p class="header-subtitle">✨ AI-Powered Spending Intelligence Dashboard &nbsp;|&nbsp; Real-time Insights &nbsp;|&nbsp; 150+ Users &nbsp;|&nbsp; 14K+ Transactions</p>
</div>
""", unsafe_allow_html=True)

    # ── Load data ─────────────────────────────────────────────
    data_path = "clean_finance_dataset.xlsx"
    if not os.path.exists(data_path):
        st.error(f"📂 Dataset not found at `{data_path}`. Please place `clean_finance_dataset.xlsx` in the same directory as `app.py` and restart.")
        st.info("**Expected location:** `./clean_finance_dataset.xlsx`")
        st.stop()

    with st.spinner("⚡ Loading & cleaning data..."):
        df = load_and_clean(data_path)

    # ── Sidebar filters ───────────────────────────────────────
    filtered_df = render_sidebar(df)

    # ── Tabs ──────────────────────────────────────────────────
    tabs = st.tabs([
        "📊 Overview",
        "📈 Trends",
        "🗺️ Locations",
        "💳 Payments",
        "👤 Users",
        "🔍 Explorer",
        "🤖 AI Insights",
    ])

    with tabs[0]:
        render_overview(filtered_df)
    with tabs[1]:
        render_trends(filtered_df)
    with tabs[2]:
        render_location(filtered_df)
    with tabs[3]:
        render_payment(filtered_df)
    with tabs[4]:
        render_users(filtered_df)
    with tabs[5]:
        render_explorer(filtered_df)
    with tabs[6]:
        render_ai_insights(filtered_df)

    # ── Footer ────────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center; padding:2rem 0 1rem; color:rgba(255,255,255,0.25); font-size:0.75rem;">
  FinanceIQ &nbsp;·&nbsp; Built with Streamlit &amp; Plotly &nbsp;·&nbsp; AI by Anthropic Claude
</div>
""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
