"""
6_What_If_Simulator.py - Interactive simulator with glassmorphism design.
"""

import streamlit as st
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.styles import inject_custom_css
from src.model_loader import load_all_models
from src.simulation import simulate_business
from src.utils import risk_badge
from config.config import NUMERIC_FEATURES, ENGINEERED_FEATURES, CLUSTER_COLORS

st.set_page_config(page_title="What-If Simulator", page_icon="🔮", layout="wide")
inject_custom_css()

st.title("🔮 What-If Simulator")
st.markdown(
    """<p style="color:#94A3B8; font-size:1rem;">
    Adjust business parameters and see how risk predictions change in real-time.
    </p>""",
    unsafe_allow_html=True,
)
st.markdown("---")

PLOTLY_BG = "rgba(0,0,0,0)"
models = load_all_models()
feature_cols = NUMERIC_FEATURES + ENGINEERED_FEATURES

# ── Input Sliders ──────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 💵 Revenue & Expenses")
    revenue_day = st.slider("Revenue per Day (₹)", 1000, 100000, 25000, step=1000)
    expense_day = st.slider("Expense per Day (₹)", 500, 80000, 18000, step=500)
    monthly_rev = revenue_day * 30
    monthly_exp = expense_day * 30
    st.caption(f"Monthly: ₹{monthly_rev:,} rev | ₹{monthly_exp:,} exp")

with col2:
    st.markdown("#### 🏦 Credit & Debt")
    credit_score = st.slider("Credit Score", 300, 900, 675, step=5)
    debt_ratio = st.slider("Debt to Revenue Ratio", 0.0, 0.50, 0.10, step=0.01)
    emi = st.slider("EMI Obligation (₹)", 0, 500000, 50000, step=5000)

with col3:
    st.markdown("#### 📊 OD & Cash Flow")
    od_required = st.slider("OD Required (₹)", 10000, 2000000, 300000, step=10000)
    od_utilization = st.slider("OD Utilization", 0.0, 1.0, 0.50, step=0.05)
    cash_inflow = st.slider("Cash Inflow (₹)", 50000, 5000000, 500000, step=50000)
    cash_outflow = st.slider("Cash Outflow (₹)", 30000, 4000000, 350000, step=50000)

st.markdown("---")
col4, _ = st.columns([1, 2])
with col4:
    st.markdown("#### 📦 Working Capital Cycle")
    inv_days = st.slider("Inventory Days", 0, 120, 35, step=5)
    recv_days = st.slider("Receivable Days", 0, 120, 40, step=5)
    pay_days = st.slider("Payable Days", 0, 120, 30, step=5)

# ── Derive features ───────────────────────────────────
profit = monthly_rev - monthly_exp
profit_margin = profit / monthly_rev if monthly_rev > 0 else 0
cash_ratio = cash_inflow / od_required if od_required > 0 else 10.0
ccc = inv_days + recv_days - pay_days

params = {
    "Revenue_per_Day": revenue_day, "Expense_per_Day": expense_day,
    "Monthly_Revenue": monthly_rev, "Monthly_Expense": monthly_exp,
    "Cash_Inflow_Adjusted": cash_inflow, "Cash_Outflow_Adjusted": cash_outflow,
    "OD_Required": od_required, "OD_Utilization": od_utilization,
    "Inventory_Days": inv_days, "Receivable_Days": recv_days, "Payable_Days": pay_days,
    "Cash_Conversion_Cycle": ccc, "Credit_Score": credit_score,
    "Debt_to_Revenue_Ratio": debt_ratio, "EMI_Obligation": emi,
    "Profit": profit, "ProfitMargin": profit_margin, "CashRatio": cash_ratio,
}

result = simulate_business(params, models, feature_cols)

# ── Results ────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🎯 Prediction Results")

cluster_color = CLUSTER_COLORS.get(result["Cluster_Name"], "#6366F1")

# Result cards with glassmorphism
st.markdown(
    f"""
    <div style="display:flex; gap:16px; flex-wrap:wrap; margin:16px 0;">
        <div style="flex:1; min-width:200px; background:rgba(30,41,59,0.45); backdrop-filter:blur(14px);
                    border:1px solid rgba(99,102,241,0.2); border-radius:16px; padding:20px; text-align:center;">
            <p style="color:#94A3B8; font-size:0.8rem; margin:0; text-transform:uppercase;">Default Probability</p>
            <p style="color:#F1F5F9; font-size:2rem; font-weight:800; margin:4px 0;">{result['PD']:.4f}</p>
            <p style="color:{'#22C55E' if result['PD']<0.05 else '#3B82F6' if result['PD']<0.10 else '#F59E0B' if result['PD']<0.15 else '#EF4444'};
               font-weight:600;">{result['Risk_Level']} Risk</p>
        </div>
        <div style="flex:1; min-width:200px; background:rgba(30,41,59,0.45); backdrop-filter:blur(14px);
                    border:1px solid rgba(99,102,241,0.2); border-radius:16px; padding:20px; text-align:center;">
            <p style="color:#94A3B8; font-size:0.8rem; margin:0; text-transform:uppercase;">OD Score</p>
            <p style="color:#F1F5F9; font-size:2rem; font-weight:800; margin:4px 0;">{result['ODScore']:.2f}</p>
            <p style="color:#A5B4FC; font-weight:600;">Suitability</p>
        </div>
        <div style="flex:1; min-width:200px; background:rgba(30,41,59,0.45); backdrop-filter:blur(14px);
                    border:1px solid {cluster_color}33; border-radius:16px; padding:20px; text-align:center;">
            <p style="color:#94A3B8; font-size:0.8rem; margin:0; text-transform:uppercase;">Cluster</p>
            <p style="color:{cluster_color}; font-size:1.5rem; font-weight:800; margin:4px 0;">{result['Cluster_Name']}</p>
            <p style="color:#94A3B8; font-weight:500;">Segment</p>
        </div>
        <div style="flex:1; min-width:200px; background:rgba(30,41,59,0.45); backdrop-filter:blur(14px);
                    border:1px solid {'#22C55E33' if result['Interest_Eligible'] else '#EF444433'};
                    border-radius:16px; padding:20px; text-align:center;">
            <p style="color:#94A3B8; font-size:0.8rem; margin:0; text-transform:uppercase;">Interest Eligible</p>
            <p style="color:{'#22C55E' if result['Interest_Eligible'] else '#EF4444'};
               font-size:2rem; font-weight:800; margin:4px 0;">{'✅ Yes' if result['Interest_Eligible'] else '❌ No'}</p>
            <p style="color:#94A3B8; font-weight:500;">Rate Reduction</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Gauge ──────────────────────────────────────────────
col_g, col_info = st.columns([2, 1])
with col_g:
    st.subheader("📊 Risk Gauge")
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=result["PD"] * 100,
        title={"text": "Default Probability (%)", "font": {"color": "#CBD5E1"}},
        number={"font": {"color": "#F1F5F9"}},
        delta={"reference": 15, "decreasing": {"color": "#22C55E"}, "increasing": {"color": "#EF4444"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#64748B"},
            "bar": {"color": "#6366F1"},
            "bgcolor": "rgba(30,41,59,0.3)",
            "steps": [
                {"range": [0, 5], "color": "rgba(34,197,94,0.3)"},
                {"range": [5, 10], "color": "rgba(59,130,246,0.3)"},
                {"range": [10, 15], "color": "rgba(245,158,11,0.3)"},
                {"range": [15, 100], "color": "rgba(239,68,68,0.3)"},
            ],
            "threshold": {"line": {"color": "#EF4444", "width": 4}, "thickness": 0.75, "value": 15},
        },
    ))
    fig.update_layout(height=300, paper_bgcolor=PLOTLY_BG, font=dict(color="#CBD5E1"))
    st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.subheader("📋 Derived Metrics")
    st.metric("💰 Monthly Profit", f"₹{profit:,}")
    st.metric("📊 Profit Margin", f"{profit_margin:.2%}")
    st.metric("🔄 Cash Conversion Cycle", f"{ccc} days")
    st.metric("💧 Cash Ratio", f"{cash_ratio:.2f}")
