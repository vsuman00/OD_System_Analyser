"""
od_scoring.py - OD Suitability Scoring.

Formula (per PRD):
    ODScore = (1 - PD) × CashRatio

Higher ODScore → business is eligible for a higher OD limit.
"""

import numpy as np
import pandas as pd


def compute_od_score(df: pd.DataFrame, pd_predictions: np.ndarray) -> pd.DataFrame:
    """
    Calculate the OD suitability score for each business.
    
    Args:
        df: DataFrame with CashRatio column
        pd_predictions: Array of predicted probability of default (PD)
    
    Returns:
        pd.DataFrame: DataFrame with new 'PD' and 'ODScore' columns
    """
    print("=" * 60)
    print("STEP 8: OD Suitability Scoring")
    print("=" * 60)
    
    # Add PD predictions to DataFrame
    df["PD"] = pd_predictions
    
    # Calculate ODScore = (1 - PD) × CashRatio
    df["ODScore"] = (1 - df["PD"]) * df["CashRatio"]
    
    # Print summary stats
    print(f"  ODScore: min={df['ODScore'].min():.4f}, max={df['ODScore'].max():.4f}, mean={df['ODScore'].mean():.4f}")
    print(f"  Top 5 businesses by ODScore:")
    top5 = df.nlargest(5, "ODScore")[["Business_ID", "Business_Type", "PD", "CashRatio", "ODScore"]]
    print(top5.to_string(index=False))
    print()
    
    return df
