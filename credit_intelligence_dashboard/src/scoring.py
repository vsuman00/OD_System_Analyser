"""
scoring.py - Risk scoring and OD suitability computation.
Uses loaded models to score individual businesses or batches.
"""

import numpy as np
import pandas as pd


def compute_risk_scores(df: pd.DataFrame, models: dict, feature_cols: list) -> pd.DataFrame:
    """
    Run the full scoring pipeline on a DataFrame:
      Scale → PCA → Cluster → ANN Predict → OD Score

    Args:
        df: DataFrame with raw + engineered features
        models: Dict with keys 'scaler', 'pca', 'kmeans', 'ann'
        feature_cols: List of feature column names to scale

    Returns:
        DataFrame with added PD, Cluster, Cluster_Name, ODScore columns
    """
    scaler = models["scaler"]
    pca = models["pca"]
    kmeans = models["kmeans"]
    ann = models["ann"]

    # Scale
    X_scaled = scaler.transform(df[feature_cols])

    # PCA
    X_pca = pca.transform(X_scaled)

    # Cluster
    clusters = kmeans.predict(X_pca)
    df = df.copy()
    df["Cluster"] = clusters

    from config.config import CLUSTER_LABELS
    df["Cluster_Name"] = df["Cluster"].map(CLUSTER_LABELS)

    # ANN predict PD
    X_ann = np.column_stack([X_pca, clusters])
    df["PD"] = ann.predict_proba(X_ann)[:, 1]

    # OD Score = (1 - PD) * CashRatio
    df["ODScore"] = (1 - df["PD"]) * df["CashRatio"]

    return df
