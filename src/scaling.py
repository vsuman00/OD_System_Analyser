"""
scaling.py - Feature scaling using StandardScaler.
Standardizes features: X_scaled = (X - mean) / std
Saves the fitted scaler for later reuse.
"""

import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from config.config import SCALER_PATH, MODELS_DIR
import os


def scale_features(df: pd.DataFrame, feature_cols: list) -> tuple:
    """
    Apply StandardScaler to the selected numeric features.
    Saves the fitted scaler to disk.
    
    Args:
        df: DataFrame with engineered features
        feature_cols: List of column names to scale
    
    Returns:
        tuple: (scaled_array, fitted_scaler)
    """
    print("=" * 60)
    print("STEP 4: Feature Scaling (StandardScaler)")
    print("=" * 60)
    
    # Create models directory if it doesn't exist
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Initialize and fit the scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[feature_cols])
    
    # Save scaler for future predictions
    joblib.dump(scaler, SCALER_PATH)
    
    print(f"  Scaled {len(feature_cols)} features")
    print(f"  Scaler saved to: {SCALER_PATH}")
    print()
    
    return X_scaled, scaler
