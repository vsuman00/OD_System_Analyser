"""
sector_analysis.py - Aggregate analysis by Business Type.
Groups results by sector to produce the final strategy report.
"""

import pandas as pd
import os
from config.config import OUTPUTS_DIR, FINAL_STRATEGY_FILE, CLUSTER_LABELS


def analyze_sectors(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate risk, OD scoring, and interest strategy data by Business_Type.
    Generates the final strategy CSV report.
    
    Args:
        df: Full DataFrame with PD, ODScore, Cluster, Interest_Reduction columns
    
    Returns:
        pd.DataFrame: Sector-level summary
    """
    print("=" * 60)
    print("STEP 10: Sector-Level Analysis & Report Generation")
    print("=" * 60)
    
    # Create outputs directory
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    
    # --- Aggregate by Business_Type ---
    sector_report = df.groupby("Business_Type").agg(
        Count=("Business_ID", "count"),
        Avg_PD=("PD", "mean"),
        Avg_ODScore=("ODScore", "mean"),
        Avg_CashRatio=("CashRatio", "mean"),
        Avg_Profit=("Profit", "mean"),
        Avg_ProfitMargin=("ProfitMargin", "mean"),
        Avg_CreditScore=("Credit_Score", "mean"),
        Interest_Reduction_Count=("Interest_Reduction", "sum"),
    ).reset_index()
    
    # Calculate the percentage eligible for interest reduction
    sector_report["Interest_Reduction_Pct"] = (
        sector_report["Interest_Reduction_Count"] / sector_report["Count"] * 100
    ).round(2)
    
    # Rank sectors by risk (lower PD = less risky)
    sector_report = sector_report.sort_values("Avg_PD", ascending=True)
    sector_report["Risk_Rank"] = range(1, len(sector_report) + 1)
    
    # --- Cluster distribution per sector ---
    if "Cluster" in df.columns:
        cluster_dist = df.groupby("Business_Type")["Cluster"].value_counts().unstack(fill_value=0)
        # Rename cluster columns
        cluster_dist.columns = [
            f"Cluster_{CLUSTER_LABELS.get(c, c)}" for c in cluster_dist.columns
        ]
        sector_report = sector_report.merge(cluster_dist, on="Business_Type", how="left")
    
    # --- Print summary ---
    print("\n  SECTOR RISK RANKING (Least Risky → Most Risky):")
    print("-" * 80)
    for _, row in sector_report.iterrows():
        print(f"  #{int(row['Risk_Rank']):2d}  {row['Business_Type']:<25s}  "
              f"Avg PD={row['Avg_PD']:.4f}  Avg ODScore={row['Avg_ODScore']:.2f}  "
              f"Interest Reduction={row['Interest_Reduction_Pct']:.1f}%")
    
    # --- Save to CSV ---
    sector_report.to_csv(FINAL_STRATEGY_FILE, index=False)
    print(f"\n  Strategy report saved to: {FINAL_STRATEGY_FILE}")
    print()
    
    return sector_report
