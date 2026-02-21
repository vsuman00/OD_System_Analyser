"""
2_Risk_Analysis.py - Risk analysis with glassmorphism design.
"""

import streamlit as st
import plotly.express as px
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.styles import inject_custom_css
from src.data_loader import load_raw_data
from src.model_loader import load_all_models
from src.scoring import compute_risk_scores
from src.utils import risk_badge
from config.config import NUMERIC_FEATURES, ENGINEERED_FEATURES

st.set_page_config(page_title="Risk Analysis", page_icon="⚠️", layout="wide")
inject_custom_css()

st.title("⚠️ Risk Analysis")
st.markdown("---")

PLOTLY_TEMPLATE = "plotly_dark"
PLOTLY_BG = "rgba(0,0,0,0)"

df = load_raw_data()
models = load_all_models()
feature_cols = NUMERIC_FEATURES + ENGINEERED_FEATURES
df = compute_risk_scores(df, models, feature_cols)

# ── Risk Band Distribution ─────────────────────────────
st.subheader("📊 Probability of Default Distribution")
col1, col2 = st.columns([2, 1])

with col1:
    fig = px.histogram(
        df, x="PD", nbins=50,
        color_discrete_sequence=["#818CF8"],
        labels={"PD": "Probability of Default"},
        template=PLOTLY_TEMPLATE,
    )
    fig.add_vline(x=0.15, line_dash="dash", line_color="#EF4444",
                  annotation_text="PD Threshold (0.15)",
                  annotation_font_color="#EF4444")
    fig.update_layout(height=400, plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                      font=dict(color="#CBD5E1"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    total = len(df)
    bands = [
        ("🟢 Very Low", "< 5%", (df["PD"] < 0.05).sum(), "#22C55E"),
        ("🔵 Low", "5-10%", ((df["PD"] >= 0.05) & (df["PD"] < 0.10)).sum(), "#3B82F6"),
        ("🟡 Medium", "10-15%", ((df["PD"] >= 0.10) & (df["PD"] < 0.15)).sum(), "#F59E0B"),
        ("🔴 High", "≥ 15%", (df["PD"] >= 0.15).sum(), "#EF4444"),
    ]
    for label, rng, count, color in bands:
        pct = count / total * 100
        st.markdown(
            f"""<div style="
                background: rgba(30,41,59,0.45); backdrop-filter: blur(12px);
                border-left: 4px solid {color}; border-radius:10px;
                padding:12px 16px; margin-bottom:8px;
            ">
                <span style="color:{color}; font-weight:700;">{label}</span>
                <span style="color:#94A3B8; font-size:0.85rem;"> ({rng})</span><br/>
                <span style="color:#F1F5F9; font-size:1.2rem; font-weight:700;">{count:,}</span>
                <span style="color:#94A3B8; font-size:0.85rem;"> ({pct:.1f}%)</span>
            </div>""",
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── PD by Sector (Box Plot) ───────────────────────────
st.subheader("📈 PD Distribution by Sector")
fig2 = px.box(
    df, x="Business_Type", y="PD",
    color="Business_Type",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    labels={"PD": "Probability of Default", "Business_Type": "Sector"},
    template=PLOTLY_TEMPLATE,
)
fig2.update_layout(height=500, showlegend=False, plot_bgcolor=PLOTLY_BG,
                   paper_bgcolor=PLOTLY_BG, font=dict(color="#CBD5E1"))
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Credit Score vs PD Scatter ─────────────────────────
st.subheader("🔍 Credit Score vs. Default Probability")
sample = df.sample(min(5000, len(df)), random_state=42)
fig3 = px.scatter(
    sample, x="Credit_Score", y="PD",
    color="Cluster_Name",
    opacity=0.5,
    labels={"Credit_Score": "Credit Score", "PD": "Probability of Default"},
    template=PLOTLY_TEMPLATE,
)
fig3.update_layout(height=500, plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                   font=dict(color="#CBD5E1"))
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── Individual Business Lookup ─────────────────────────
st.subheader("🔎 Business Lookup")
business_id = st.text_input("Enter Business ID (e.g., B1234):", "")
if business_id:
    match = df[df["Business_ID"] == business_id]
    if len(match) == 0:
        st.warning(f"No business found with ID: {business_id}")
    else:
        row = match.iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Business Type", row["Business_Type"])
        c2.metric("Risk Level", risk_badge(row["PD"]))
        c3.metric("PD", f"{row['PD']:.4f}")
        c4.metric("OD Score", f"{row['ODScore']:.2f}")

        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Cluster", row["Cluster_Name"])
        c6.metric("Credit Score", f"{row['Credit_Score']:.0f}")
        c7.metric("Profit", f"₹{row['Profit']:,.0f}")
        c8.metric("OD Utilization", f"{row['OD_Utilization']:.2%}")
