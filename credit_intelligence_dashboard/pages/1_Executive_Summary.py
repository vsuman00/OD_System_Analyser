"""
1_Executive_Summary.py - High-level KPI dashboard with glassmorphism design.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.styles import inject_custom_css
from src.data_loader import load_raw_data, load_strategy_report
from src.model_loader import load_all_models
from src.scoring import compute_risk_scores
from config.config import NUMERIC_FEATURES, ENGINEERED_FEATURES, CLUSTER_COLORS

st.set_page_config(page_title="Executive Summary", page_icon="📊", layout="wide")
inject_custom_css()

st.title("📊 Executive Summary")
st.markdown("---")

# Load and score data
df = load_raw_data()
models = load_all_models()
feature_cols = NUMERIC_FEATURES + ENGINEERED_FEATURES
df = compute_risk_scores(df, models, feature_cols)
strategy = load_strategy_report()

PLOTLY_TEMPLATE = "plotly_dark"
PLOTLY_BG = "rgba(0,0,0,0)"
PLOTLY_PAPER = "rgba(0,0,0,0)"

# ── Top KPI Row ────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏢 Total Businesses", f"{len(df):,}")
col2.metric("📉 Avg Default Probability", f"{df['PD'].mean():.4f}")
col3.metric("⭐ Avg OD Score", f"{df['ODScore'].mean():.2f}")
col4.metric("💰 Interest Eligible",
            f"{((df['PD'] < 0.15) & (df['OD_Utilization'] > 0.70)).sum():,}")

st.markdown("---")

# ── Sector Risk Ranking ────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏆 Sector Risk Ranking")
    fig = px.bar(
        strategy.sort_values("Avg_PD"),
        x="Avg_PD", y="Business_Type",
        orientation="h",
        color="Avg_PD",
        color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"],
        labels={"Avg_PD": "Avg Probability of Default", "Business_Type": "Sector"},
        template=PLOTLY_TEMPLATE,
    )
    fig.update_layout(
        height=400, yaxis=dict(autorange="reversed"), showlegend=False,
        plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_PAPER,
        font=dict(color="#CBD5E1"),
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("📊 Cluster Distribution")
    cluster_counts = df["Cluster_Name"].value_counts().reset_index()
    cluster_counts.columns = ["Cluster", "Count"]
    fig2 = px.pie(
        cluster_counts, names="Cluster", values="Count",
        color="Cluster",
        color_discrete_map=CLUSTER_COLORS,
        hole=0.45,
        template=PLOTLY_TEMPLATE,
    )
    fig2.update_layout(
        height=400,
        plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_PAPER,
        font=dict(color="#CBD5E1"),
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── OD Score by Sector ─────────────────────────────────
st.subheader("💳 Average OD Suitability Score by Sector")
fig3 = px.bar(
    strategy.sort_values("Avg_ODScore", ascending=False),
    x="Business_Type", y="Avg_ODScore",
    color="Avg_ODScore",
    color_continuous_scale=["#312E81", "#6366F1", "#A5B4FC"],
    labels={"Avg_ODScore": "Avg OD Score", "Business_Type": "Sector"},
    template=PLOTLY_TEMPLATE,
)
fig3.update_layout(
    height=400,
    plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_PAPER,
    font=dict(color="#CBD5E1"),
)
st.plotly_chart(fig3, use_container_width=True)

# ── Strategy Table ─────────────────────────────────────
st.subheader("📋 Full Sector Strategy Table")
display_cols = [
    "Risk_Rank", "Business_Type", "Count", "Avg_PD", "Avg_ODScore",
    "Avg_CashRatio", "Avg_CreditScore", "Interest_Reduction_Pct",
]
st.dataframe(
    strategy[display_cols].style.format({
        "Avg_PD": "{:.4f}",
        "Avg_ODScore": "{:.2f}",
        "Avg_CashRatio": "{:.2f}",
        "Avg_CreditScore": "{:.0f}",
        "Interest_Reduction_Pct": "{:.2f}%",
    }),
    width="stretch",
    hide_index=True,
)
