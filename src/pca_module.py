"""
pca_module.py - Principal Component Analysis for dimensionality reduction.
Retains 95% of explained variance to reduce feature space while preserving information.
"""

import numpy as np
import joblib
from sklearn.decomposition import PCA
from config.config import PCA_VARIANCE_THRESHOLD, PCA_PATH, MODELS_DIR
import os


def apply_pca(X_scaled: np.ndarray) -> tuple:
    """
    Apply PCA to the scaled feature matrix.
    Retains components that explain >= 95% of total variance.
    
    Args:
        X_scaled: Scaled feature matrix (numpy array)
    
    Returns:
        tuple: (X_pca, fitted_pca_model)
    """
    print("=" * 60)
    print("STEP 5: PCA (Dimensionality Reduction)")
    print("=" * 60)
    
    # Create models directory if it doesn't exist
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Fit PCA with 95% variance retention
    pca = PCA(n_components=PCA_VARIANCE_THRESHOLD, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
    # Print results
    print(f"  Original features    : {X_scaled.shape[1]}")
    print(f"  PCA components kept  : {pca.n_components_}")
    print(f"  Variance retained    : {sum(pca.explained_variance_ratio_):.4f}")
    print(f"  Variance per component: {np.round(pca.explained_variance_ratio_, 4)}")
    
    # Save PCA model
    joblib.dump(pca, PCA_PATH)
    print(f"  PCA model saved to   : {PCA_PATH}")
    print()
    
    return X_pca, pca
