"""
sector_analysis.py - Sector-level aggregation for dashboard views.
"""

import pandas as pd
import numpy as np


def get_sector_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate key metrics by Business_Type.

    Returns DataFrame with: Count, Avg_PD, Avg_ODScore, Avg_Profit,
    Avg_CreditScore, Interest_Eligible_Pct, and cluster distribution.
    """
    from config.config import PD_THRESHOLD, OD_UTIL_THRESHOLD

    # Flag interest reduction eligible
    df = df.copy()
    df["Interest_Eligible"] = (df["PD"] < PD_THRESHOLD) & (df["OD_Utilization"] > OD_UTIL_THRESHOLD)

    summary = df.groupby("Business_Type").agg(
        Count=("Business_ID", "count"),
        Avg_PD=("PD", "mean"),
        Avg_ODScore=("ODScore", "mean"),
        Avg_Profit=("Profit", "mean"),
        Avg_ProfitMargin=("ProfitMargin", "mean"),
        Avg_CashRatio=("CashRatio", "mean"),
        Avg_CreditScore=("Credit_Score", "mean"),
        Avg_OD_Utilization=("OD_Utilization", "mean"),
        Interest_Eligible_Count=("Interest_Eligible", "sum"),
    ).reset_index()

    summary["Interest_Eligible_Pct"] = (
        summary["Interest_Eligible_Count"] / summary["Count"] * 100
    ).round(2)
    summary = summary.sort_values("Avg_PD")
    summary["Risk_Rank"] = range(1, len(summary) + 1)

    return summary


def get_cluster_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Get cluster distribution per sector."""
    return df.groupby(["Business_Type", "Cluster_Name"]).size().reset_index(name="Count")
