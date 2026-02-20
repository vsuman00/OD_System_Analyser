"""
interest_strategy.py - Interest rate reduction strategy.

Rule (per PRD):
    Reduce interest when: PD < 0.15 AND OD_Utilization > 70%
    
Purpose: Encourage safe businesses to expand their OD usage.
"""

import pandas as pd
from config.config import PD_THRESHOLD, OD_UTIL_THRESHOLD


def apply_interest_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag businesses eligible for interest rate reduction.
    
    Criteria:
        - Probability of Default (PD) < 0.15  (low risk)
        - OD Utilization > 0.70               (active OD user)
    
    Args:
        df: DataFrame with 'PD' and 'OD_Utilization' columns
    
    Returns:
        pd.DataFrame: DataFrame with new 'Interest_Reduction' column (True/False)
    """
    print("=" * 60)
    print("STEP 9: Interest Reduction Strategy")
    print("=" * 60)
    
    # Apply the rule: PD < threshold AND OD_Utilization > threshold
    df["Interest_Reduction"] = (
        (df["PD"] < PD_THRESHOLD) & (df["OD_Utilization"] > OD_UTIL_THRESHOLD)
    )
    
    # Count eligible businesses
    eligible = df["Interest_Reduction"].sum()
    total = len(df)
    
    print(f"  Criteria: PD < {PD_THRESHOLD} AND OD_Utilization > {OD_UTIL_THRESHOLD}")
    print(f"  Eligible for interest reduction: {eligible} / {total} ({eligible/total*100:.1f}%)")
    print()
    
    return df
