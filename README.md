# 💰 FinanceIQ — AI-Powered Personal Finance Analytics Dashboard

A production-ready, visually stunning **Streamlit** dashboard for personal finance analytics, powered by **Claude AI** (Anthropic).

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://financeiq.streamlit.app)

---

## ✨ Features

- 📊 **Overview** — KPI cards, monthly income/expense charts, category breakdown, daily trend with moving average  
- 📈 **Trends & Time Analysis** — Monthly heatmap, quarterly breakdown, day-of-week radar chart, savings rate  
- 🗺️ **Location Intelligence** — City-wise spending, treemaps, city × category heatmap  
- 💳 **Payment Analysis** — Mode distribution, trends over time, cash vs digital ratio  
- 👤 **User Analytics** — Top spenders, scatter plots, single-user deep dive  
- 🔍 **Transaction Explorer** — Search, filter, download CSV, summary stats  
- 🤖 **AI Insights** — Claude-powered financial health analysis & Q&A  

## 🚀 Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Place `clean_finance_dataset.xlsx` in the root directory before running.

## 🤖 AI Insights Setup

Set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Or add it to `.streamlit/secrets.toml` (for Streamlit Cloud):

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

## 📦 Dataset

- **14,538 rows × 9 columns**
- 150 unique users across 10 Indian cities
- Covers income, expenses, payment modes, and categories

## 🛠️ Tech Stack

- **Frontend**: Streamlit + Custom CSS (Glassmorphism, animations)
- **Charts**: Plotly (dark theme, transparent backgrounds)
- **AI**: Anthropic Claude Sonnet
- **Data**: Pandas + OpenPyXL

## 👤 Author

**pmb20** — [GitHub](https://github.com/pmb20) | 23eg107b48@anurag.edu.in
