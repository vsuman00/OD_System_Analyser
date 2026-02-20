"""
feature_engineering.py - Create derived features as per PRD.

Engineered Features:
    Profit       = Monthly_Revenue - Monthly_Expense
    ProfitMargin = Profit / Monthly_Revenue
    CashRatio    = Cash_Inflow_Adjusted / OD_Required  (safe division)
    CCC          = Inventory_Days + Receivable_Days - Payable_Days
"""

import pandas as pd
import numpy as np


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create new features from existing columns.
    
    Args:
        df: Preprocessed DataFrame
    
    Returns:
        pd.DataFrame: DataFrame with new engineered columns added
    """
    print("=" * 60)
    print("STEP 3: Feature Engineering")
    print("=" * 60)
    
    # --- Profit = Revenue - Expense ---
    df["Profit"] = df["Monthly_Revenue"] - df["Monthly_Expense"]
    print("  Created: Profit = Monthly_Revenue - Monthly_Expense")
    
    # --- ProfitMargin = Profit / Revenue (handle zero revenue) ---
    df["ProfitMargin"] = np.where(
        df["Monthly_Revenue"] != 0,
        df["Profit"] / df["Monthly_Revenue"],
        0.0
    )
    print("  Created: ProfitMargin = Profit / Monthly_Revenue")
    
    # --- CashRatio = CashInflow / ODRequired (avoid divide-by-zero) ---
    # If OD_Required is 0, business doesn't need OD, so CashRatio = high value (capped at 10)
    df["CashRatio"] = np.where(
        df["OD_Required"] > 0,
        df["Cash_Inflow_Adjusted"] / df["OD_Required"],
        10.0  # Cap for businesses with no OD requirement
    )
    print("  Created: CashRatio = Cash_Inflow_Adjusted / OD_Required")
    
    # --- CCC (already in dataset, but recalculate for consistency) ---
    df["CCC_Calculated"] = (
        df["Inventory_Days"] + df["Receivable_Days"] - df["Payable_Days"]
    )
    print("  Created: CCC_Calculated = Inventory + Receivable - Payable")
    
    print(f"  New columns added: Profit, ProfitMargin, CashRatio, CCC_Calculated")
    print()
    
    return df
