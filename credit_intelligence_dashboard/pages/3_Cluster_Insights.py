"""
3_Cluster_Insights.py - K-Means cluster profiling with glassmorphism design.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.styles import inject_custom_css
from src.data_loader import load_raw_data
from src.model_loader import load_all_models
from src.scoring import compute_risk_scores
from config.config import NUMERIC_FEATURES, ENGINEERED_FEATURES, CLUSTER_COLORS, CLUSTER_LABELS

st.set_page_config(page_title="Cluster Insights", page_icon="🎯", layout="wide")
inject_custom_css()

st.title("🎯 Cluster Insights")
st.markdown("---")

PLOTLY_BG = "rgba(0,0,0,0)"

df = load_raw_data()
models = load_all_models()
feature_cols = NUMERIC_FEATURES + ENGINEERED_FEATURES
df = compute_risk_scores(df, models, feature_cols)

# ── Cluster KPI Cards ──────────────────────────────────
cols = st.columns(4)
for i, (cluster_id, name) in enumerate(CLUSTER_LABELS.items()):
    subset = df[df["Cluster"] == cluster_id]
    color = CLUSTER_COLORS.get(name, "#888")
    cols[i].markdown(
        f"""<div style="
            background: rgba(30,41,59,0.45); backdrop-filter: blur(16px);
            border: 1px solid {color}44; border-radius:16px;
            padding:20px; text-align:center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        ">
            <div style="
                width:48px; height:48px; border-radius:12px;
                background: {color}22; display:inline-flex;
                align-items:center; justify-content:center;
                border: 1px solid {color}44; margin-bottom:12px;
            ">
                <span style="font-size:1.4rem;">{'🛡️' if i==0 else '📈' if i==1 else '⚡' if i==2 else '🔥'}</span>
            </div>
            <h4 style="color:{color}; margin:0; font-weight:700;">{name}</h4>
            <p style="color:#94A3B8; font-size:0.8rem; margin:4px 0;">Businesses</p>
            <p style="color:#F1F5F9; font-size:1.5rem; font-weight:700; margin:0;">{len(subset):,}</p>
            <div style="display:flex; justify-content:space-around; margin-top:12px; padding-top:12px;
                        border-top:1px solid rgba(255,255,255,0.06);">
                <div>
                    <p style="color:#94A3B8; font-size:0.7rem; margin:0;">Avg PD</p>
                    <p style="color:#E2E8F0; font-weight:600; margin:0;">{subset['PD'].mean():.4f}</p>
                </div>
                <div>
                    <p style="color:#94A3B8; font-size:0.7rem; margin:0;">OD Score</p>
                    <p style="color:#E2E8F0; font-weight:600; margin:0;">{subset['ODScore'].mean():.2f}</p>
                </div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Cluster Distribution by Sector ─────────────────────
st.subheader("📊 Cluster Distribution by Sector")
cluster_sector = df.groupby(["Business_Type", "Cluster_Name"]).size().reset_index(name="Count")
fig = px.bar(
    cluster_sector, x="Business_Type", y="Count",
    color="Cluster_Name",
    color_discrete_map=CLUSTER_COLORS,
    barmode="group",
    labels={"Business_Type": "Sector", "Cluster_Name": "Cluster"},
    template="plotly_dark",
)
fig.update_layout(height=500, plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                  font=dict(color="#CBD5E1"))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Radar Chart ────────────────────────────────────────
st.subheader("🕸️ Cluster Profiles")
radar_metrics = ["PD", "ODScore", "CashRatio", "ProfitMargin", "OD_Utilization", "Credit_Score"]
cluster_means = df.groupby("Cluster_Name")[radar_metrics].mean()
normalized = (cluster_means - cluster_means.min()) / (cluster_means.max() - cluster_means.min() + 1e-10)

fig2 = go.Figure()
for cluster_name in normalized.index:
    values = normalized.loc[cluster_name].tolist()
    values.append(values[0])
    categories = radar_metrics + [radar_metrics[0]]
    fig2.add_trace(go.Scatterpolar(
        r=values, theta=categories, fill="toself", name=cluster_name,
        line_color=CLUSTER_COLORS.get(cluster_name, "#888"),
    ))
fig2.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(99,102,241,0.15)"),
        angularaxis=dict(gridcolor="rgba(99,102,241,0.15)"),
        bgcolor="rgba(0,0,0,0)",
    ),
    height=500, showlegend=True, template="plotly_dark",
    plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG, font=dict(color="#CBD5E1"),
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── 3D PCA ─────────────────────────────────────────────
st.subheader("🌐 3D PCA Projection")
scaler = models["scaler"]
pca_model = models["pca"]
X_scaled = scaler.transform(df[feature_cols])
X_pca = pca_model.transform(X_scaled)

sample_idx = np.random.choice(len(df), size=min(8000, len(df)), replace=False)
pca_df = pd.DataFrame({
    "PC1": X_pca[sample_idx, 0], "PC2": X_pca[sample_idx, 1], "PC3": X_pca[sample_idx, 2],
    "Cluster": df.iloc[sample_idx]["Cluster_Name"].values,
})

fig3 = px.scatter_3d(
    pca_df, x="PC1", y="PC2", z="PC3",
    color="Cluster", color_discrete_map=CLUSTER_COLORS,
    opacity=0.5, size_max=3, template="plotly_dark",
)
fig3.update_layout(height=600, plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                   font=dict(color="#CBD5E1"))
st.plotly_chart(fig3, use_container_width=True)
