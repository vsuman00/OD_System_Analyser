"""
4_OD_Optimization.py - OD suitability analysis with glassmorphism design.
"""

import streamlit as st
import plotly.express as px
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.styles import inject_custom_css
from src.data_loader import load_raw_data
from src.model_loader import load_all_models
from src.scoring import compute_risk_scores
from config.config import NUMERIC_FEATURES, ENGINEERED_FEATURES

st.set_page_config(page_title="OD Optimization", page_icon="💳", layout="wide")
inject_custom_css()

st.title("💳 OD Limit Optimization")
st.markdown("---")

PLOTLY_BG = "rgba(0,0,0,0)"

df = load_raw_data()
models = load_all_models()
feature_cols = NUMERIC_FEATURES + ENGINEERED_FEATURES
df = compute_risk_scores(df, models, feature_cols)

# ── KPIs ───────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("⭐ Avg OD Score", f"{df['ODScore'].mean():.2f}")
c2.metric("📊 Median OD Score", f"{df['ODScore'].median():.2f}")
c3.metric("✅ High Suitability (>10)", f"{(df['ODScore'] > 10).sum():,}")
c4.metric("⚠️ Low Suitability (<1)", f"{(df['ODScore'] < 1).sum():,}")

st.markdown("---")

# ── ODScore by Sector ──────────────────────────────────
st.subheader("📊 OD Score Distribution by Sector")
fig = px.box(
    df, x="Business_Type", y="ODScore", color="Business_Type",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    labels={"ODScore": "OD Suitability Score", "Business_Type": "Sector"},
    template="plotly_dark",
)
fig.update_layout(height=500, showlegend=False, plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                  font=dict(color="#CBD5E1"), yaxis=dict(range=[0, df["ODScore"].quantile(0.95)]))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Scatter ────────────────────────────────────────────
col_l, col_r = st.columns(2)
sample = df.sample(min(5000, len(df)), random_state=42)

with col_l:
    st.subheader("🔗 OD Score vs Cash Ratio")
    fig2 = px.scatter(
        sample, x="CashRatio", y="ODScore", color="Cluster_Name", opacity=0.5,
        labels={"CashRatio": "Cash Ratio", "ODScore": "OD Score"},
        template="plotly_dark",
    )
    fig2.update_layout(height=450, plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                       font=dict(color="#CBD5E1"),
                       xaxis=dict(range=[0, sample["CashRatio"].quantile(0.95)]),
                       yaxis=dict(range=[0, sample["ODScore"].quantile(0.95)]))
    st.plotly_chart(fig2, use_container_width=True)

with col_r:
    st.subheader("📉 OD Score vs PD")
    fig3 = px.scatter(
        sample, x="PD", y="ODScore", color="Cluster_Name", opacity=0.5,
        labels={"PD": "Probability of Default", "ODScore": "OD Score"},
        template="plotly_dark",
    )
    fig3.update_layout(height=450, plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                       font=dict(color="#CBD5E1"),
                       yaxis=dict(range=[0, sample["ODScore"].quantile(0.95)]))
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── Top & Bottom Tables ────────────────────────────────
st.subheader("🏆 Top 20 Businesses by OD Score")
top_20 = df.nlargest(20, "ODScore")[
    ["Business_ID", "Business_Type", "PD", "CashRatio", "ODScore", "Cluster_Name", "Credit_Score"]
]
st.dataframe(top_20, width="stretch", hide_index=True)

st.subheader("⚠️ Bottom 20 Businesses by OD Score")
bottom_20 = df.nsmallest(20, "ODScore")[
    ["Business_ID", "Business_Type", "PD", "CashRatio", "ODScore", "Cluster_Name", "Credit_Score"]
]
st.dataframe(bottom_20, width="stretch", hide_index=True)
