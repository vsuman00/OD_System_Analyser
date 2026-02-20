"""
data_loader.py - Load the business financial stress dataset from CSV.
Provides a simple function to read data and print basic info.
"""

import pandas as pd
from config.config import DATA_FILE


def load_data() -> pd.DataFrame:
    """
    Load the CSV dataset into a pandas DataFrame.
    Prints dataset shape and basic info for verification.
    
    Returns:
        pd.DataFrame: Raw dataset
    """
    print("=" * 60)
    print("STEP 1: Loading Data")
    print("=" * 60)
    
    # Read CSV file
    df = pd.read_csv(DATA_FILE)
    
    # Print basic info
    print(f"  Dataset shape : {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"  Columns       : {list(df.columns)}")
    print(f"  Missing values: {df.isnull().sum().sum()}")
    print()
    
    return df
