"""
preprocessing.py - Data cleaning and preprocessing.
Handles missing values, duplicates, and prepares the dataset for analysis.
"""

import pandas as pd


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the raw dataset.
    
    Steps:
        1. Drop duplicate rows
        2. Fill missing numeric values with column median
        3. Drop rows with missing Business_Type
    
    Args:
        df: Raw DataFrame from data_loader
    
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    print("=" * 60)
    print("STEP 2: Preprocessing / Cleaning Data")
    print("=" * 60)
    
    initial_rows = len(df)
    
    # --- Drop duplicates ---
    df = df.drop_duplicates()
    print(f"  Duplicates removed  : {initial_rows - len(df)}")
    
    # --- Fill missing numeric values with median ---
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"  Filled missing '{col}' with median = {median_val:.2f}")
    
    # --- Drop rows where Business_Type is missing ---
    if df["Business_Type"].isnull().sum() > 0:
        before = len(df)
        df = df.dropna(subset=["Business_Type"])
        print(f"  Dropped {before - len(df)} rows with missing Business_Type")
    
    print(f"  Final dataset shape : {df.shape}")
    print()
    
    return df.reset_index(drop=True)
