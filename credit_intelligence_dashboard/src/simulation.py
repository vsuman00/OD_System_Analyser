"""
simulation.py - What-If Simulator engine.
Allows users to input custom business parameters and get predicted PD,
cluster assignment, ODScore, and interest reduction eligibility.
"""

import numpy as np
import pandas as pd


def simulate_business(params: dict, models: dict, feature_cols: list) -> dict:
    """
    Simulate a single business through the ML pipeline.

    Args:
        params: Dict of feature values keyed by column name
        models: Dict with 'scaler', 'pca', 'kmeans', 'ann'
        feature_cols: Ordered list of feature column names

    Returns:
        Dict with PD, Cluster, Cluster_Name, ODScore, Interest_Eligible
    """
    from config.config import CLUSTER_LABELS, PD_THRESHOLD, OD_UTIL_THRESHOLD

    # Build feature vector in correct order
    X = np.array([[params.get(f, 0.0) for f in feature_cols]])

    # Scale
    X_scaled = models["scaler"].transform(X)
    # PCA
    X_pca = models["pca"].transform(X_scaled)
    # Cluster
    cluster = models["kmeans"].predict(X_pca)[0]
    cluster_name = CLUSTER_LABELS.get(cluster, f"Cluster {cluster}")
    # ANN predict PD
    X_ann = np.column_stack([X_pca, [cluster]])
    pd_score = models["ann"].predict_proba(X_ann)[0, 1]

    # OD Score
    cash_ratio = params.get("CashRatio", 1.0)
    od_score = (1 - pd_score) * cash_ratio

    # Interest eligible
    od_util = params.get("OD_Utilization", 0.0)
    interest_eligible = (pd_score < PD_THRESHOLD) and (od_util > OD_UTIL_THRESHOLD)

    return {
        "PD": round(pd_score, 6),
        "Cluster": cluster,
        "Cluster_Name": cluster_name,
        "ODScore": round(od_score, 4),
        "Interest_Eligible": interest_eligible,
        "Risk_Level": "Low" if pd_score < 0.10 else ("Medium" if pd_score < 0.30 else "High"),
    }
