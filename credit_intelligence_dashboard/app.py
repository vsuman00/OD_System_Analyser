"""
app.py - Main entry point for the Credit Intelligence Dashboard.
Streamlit multi-page app with glassmorphism dark theme.

Run with:
    streamlit run app.py
"""

import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.styles import inject_custom_css

# ── Page Configuration ─────────────────────────────────
st.set_page_config(
    page_title="Credit Intelligence Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject Glassmorphism CSS ───────────────────────────
inject_custom_css()

# ── Sidebar ────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏦 Credit Intelligence")
    st.markdown("---")
    st.markdown(
        """
        **Navigate** to explore:
        - 📊 Executive Summary
        - ⚠️ Risk Analysis
        - 🎯 Cluster Insights
        - 💳 OD Optimization
        - 💰 Interest Strategy
        - 🔮 What-If Simulator
        """
    )
    st.markdown("---")
    st.caption("Powered by PCA + K-Means + ANN")
    st.caption("Dataset: 100K Business Records")

# ── Home Page ──────────────────────────────────────────
st.title("🏦 Credit Intelligence Dashboard")

st.markdown(
    """
    <div style="
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 20px;
        padding: 32px;
        margin: 16px 0 28px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    ">
        <h3 style="color:#A5B4FC; margin-top:0;">Intelligent OD Risk & Strategy Optimization System</h3>
        <p style="color:#CBD5E1; font-size:1.05rem; line-height:1.7;">
            An interactive platform for analyzing business credit risk, optimizing
            Overdraft limits, and implementing intelligent interest rate strategies
            — powered by PCA, K-Means & ANN on 100K business records.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Tech Stack Cards ───────────────────────────────────
st.markdown("### ⚙️ Technology Stack")
cols = st.columns(5)
tech_items = [
    ("🔬", "PCA", "18 → 10 features", "#6366F1"),
    ("🎯", "K-Means", "4 Clusters", "#8B5CF6"),
    ("🧠", "ANN", "256→128→64", "#A78BFA"),
    ("📊", "OD Score", "(1-PD)×CashRatio", "#C4B5FD"),
    ("💰", "Strategy", "PD<0.15 & OD>70%", "#DDD6FE"),
]
for col, (icon, title, desc, color) in zip(cols, tech_items):
    col.markdown(
        f"""
        <div style="
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(14px);
            border: 1px solid {color}33;
            border-radius: 16px;
            padding: 20px 16px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            min-height: 140px;
        ">
            <div style="font-size:2rem; margin-bottom:8px;">{icon}</div>
            <div style="color:{color}; font-weight:700; font-size:1rem;">{title}</div>
            <div style="color:#94A3B8; font-size:0.82rem; margin-top:4px;">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Quick Stats ────────────────────────────────────────
try:
    from src.data_loader import load_raw_data
    from src.model_loader import load_all_models
    from src.scoring import compute_risk_scores
    from config.config import NUMERIC_FEATURES, ENGINEERED_FEATURES

    df = load_raw_data()
    models = load_all_models()
    feature_cols = NUMERIC_FEATURES + ENGINEERED_FEATURES
    df = compute_risk_scores(df, models, feature_cols)

    st.markdown("### 📈 Live System Metrics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏢 Total Businesses", f"{len(df):,}")
    c2.metric("📉 Avg Default Probability", f"{df['PD'].mean():.4f}")
    c3.metric("⭐ Avg OD Score", f"{df['ODScore'].mean():.2f}")
    eligible = ((df['PD'] < 0.15) & (df['OD_Utilization'] > 0.70)).sum()
    c4.metric("💰 Interest Eligible", f"{eligible:,}")
except Exception:
    st.info("👈 Navigate to individual pages to explore the data.")

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#64748B; font-size:0.8rem;'>"
    "👈 Use the sidebar to navigate between dashboard pages</p>",
    unsafe_allow_html=True,
)
