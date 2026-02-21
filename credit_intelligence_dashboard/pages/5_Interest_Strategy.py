"""
5_Interest_Strategy.py - Interest rate reduction strategy with glassmorphism design.
"""

import streamlit as st
import plotly.express as px
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.styles import inject_custom_css
from src.data_loader import load_raw_data
from src.model_loader import load_all_models
from src.scoring import compute_risk_scores
from config.config import NUMERIC_FEATURES, ENGINEERED_FEATURES, PD_THRESHOLD, OD_UTIL_THRESHOLD

st.set_page_config(page_title="Interest Strategy", page_icon="💰", layout="wide")
inject_custom_css()

st.title("💰 Interest Rate Strategy")
st.markdown("---")

PLOTLY_BG = "rgba(0,0,0,0)"

df = load_raw_data()
models = load_all_models()
feature_cols = NUMERIC_FEATURES + ENGINEERED_FEATURES
df = compute_risk_scores(df, models, feature_cols)
df["Interest_Eligible"] = (df["PD"] < PD_THRESHOLD) & (df["OD_Utilization"] > OD_UTIL_THRESHOLD)

eligible = df[df["Interest_Eligible"]]

# ── KPIs ───────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("📋 Total Businesses", f"{len(df):,}")
c2.metric("✅ Eligible for Reduction", f"{len(eligible):,}")
c3.metric("📊 Eligibility Rate", f"{len(eligible)/len(df)*100:.1f}%")
c4.metric("📉 Avg PD of Eligible", f"{eligible['PD'].mean():.4f}")

st.markdown("---")

# ── Criteria Banner ────────────────────────────────────
st.markdown(
    f"""<div style="
        background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1));
        backdrop-filter: blur(14px); border: 1px solid rgba(99,102,241,0.25);
        border-radius: 14px; padding: 20px 28px;
    ">
        <span style="color:#A5B4FC; font-weight:700; font-size:1.05rem;">📐 Reduction Criteria:</span>
        <span style="color:#E2E8F0; font-size:1rem;">
            PD &lt; {PD_THRESHOLD} (low risk) <b>AND</b> OD Utilization &gt; {OD_UTIL_THRESHOLD:.0%} (active user)
        </span>
    </div>""",
    unsafe_allow_html=True,
)
st.markdown("")

# ── PD vs OD Utilization Scatter ───────────────────────
st.subheader("🔍 Eligibility Map")
sample = df.sample(min(8000, len(df)), random_state=42).copy()
sample["Eligible"] = sample["Interest_Eligible"].map({True: "Eligible ✅", False: "Not Eligible"})

fig = px.scatter(
    sample, x="OD_Utilization", y="PD", color="Eligible",
    color_discrete_map={"Eligible ✅": "#22C55E", "Not Eligible": "#475569"},
    opacity=0.5, template="plotly_dark",
    labels={"OD_Utilization": "OD Utilization", "PD": "Probability of Default"},
)
fig.add_hline(y=PD_THRESHOLD, line_dash="dash", line_color="#EF4444",
              annotation_text=f"PD = {PD_THRESHOLD}", annotation_font_color="#EF4444")
fig.add_vline(x=OD_UTIL_THRESHOLD, line_dash="dash", line_color="#6366F1",
              annotation_text=f"OD = {OD_UTIL_THRESHOLD:.0%}", annotation_font_color="#A5B4FC")
fig.update_layout(height=500, plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                  font=dict(color="#CBD5E1"))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Sector Breakdown ───────────────────────────────────
st.subheader("📊 Eligibility by Sector")
sector_elig = df.groupby("Business_Type").agg(
    Total=("Business_ID", "count"), Eligible=("Interest_Eligible", "sum"),
).reset_index()
sector_elig["Eligible_Pct"] = (sector_elig["Eligible"] / sector_elig["Total"] * 100).round(2)
sector_elig = sector_elig.sort_values("Eligible_Pct", ascending=False)

fig2 = px.bar(
    sector_elig, x="Business_Type", y="Eligible_Pct",
    color="Eligible_Pct", color_continuous_scale=["#312E81", "#6366F1", "#22C55E"],
    labels={"Eligible_Pct": "% Eligible", "Business_Type": "Sector"},
    text="Eligible_Pct", template="plotly_dark",
)
fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig2.update_layout(height=450, plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                   font=dict(color="#CBD5E1"))
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Cluster Pie + Sample Table ─────────────────────────
col_l, col_r = st.columns(2)
with col_l:
    st.subheader("🎯 By Cluster")
    cluster_elig = df.groupby("Cluster_Name").agg(
        Total=("Business_ID", "count"), Eligible=("Interest_Eligible", "sum"),
    ).reset_index()
    fig3 = px.pie(
        cluster_elig, names="Cluster_Name", values="Eligible", hole=0.45,
        color_discrete_sequence=["#6366F1", "#8B5CF6", "#A78BFA", "#C4B5FD"],
        template="plotly_dark",
    )
    fig3.update_layout(height=400, plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                       font=dict(color="#CBD5E1"))
    st.plotly_chart(fig3, use_container_width=True)

with col_r:
    st.subheader("📋 Eligible Sample")
    if len(eligible) > 0:
        st.dataframe(
            eligible.sample(min(15, len(eligible)), random_state=42)[
                ["Business_ID", "Business_Type", "PD", "OD_Utilization", "ODScore", "Cluster_Name"]
            ].reset_index(drop=True),
            width="stretch", hide_index=True,
        )
