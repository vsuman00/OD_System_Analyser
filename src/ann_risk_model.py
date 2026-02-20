"""
ann_risk_model.py - Artificial Neural Network for risk prediction.

Architecture (based on PRD, implemented via sklearn MLPClassifier):
    Input  → PCA components + Cluster label
    Layer1 → 256 neurons (ReLU)
    Layer2 → 128 neurons (ReLU)
    Layer3 → 64 neurons  (ReLU)
    Output → 1 neuron (Sigmoid / Logistic) → Probability of Default (PD)
 
Note: Uses scikit-learn MLPClassifier which implements a multi-layer
      perceptron with backpropagation (functionally equivalent to a
      Keras Sequential ANN for binary classification).
"""

import numpy as np
import os
import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from config.config import (
    ANN_LAYERS, ANN_EPOCHS, ANN_BATCH_SIZE,
    ANN_MODEL_PATH, MODELS_DIR, RANDOM_SEED,
)


def create_risk_label(df) -> np.ndarray:
    """
    Create a proxy risk label for training.
    A business is considered 'high risk' (label=1) if:
        - OD_Utilization > 0.7  (high credit stress)
        - Debt_to_Revenue_Ratio > 0.15 (high debt burden)
        - Credit_Score < 600 (poor credit)
    Any TWO of the three conditions met → high risk.
    
    Args:
        df: DataFrame with required columns
    
    Returns:
        np.ndarray: Binary risk labels (0=low risk, 1=high risk)
    """
    # Count how many risk conditions are met per business
    risk_score = (
        (df["OD_Utilization"] > 0.7).astype(int)
        + (df["Debt_to_Revenue_Ratio"] > 0.15).astype(int)
        + (df["Credit_Score"] < 600).astype(int)
    )
    # High risk if 2 or more conditions are met
    risk_label = (risk_score >= 2).astype(int)
    return risk_label.values


def build_ann(input_dim: int) -> MLPClassifier:
    """
    Build the ANN model using sklearn MLPClassifier.
    Architecture: 256 → 128 → 64 hidden layers with ReLU activation.
    
    Args:
        input_dim: Number of input features (PCA components + cluster label)
    
    Returns:
        MLPClassifier: Configured (untrained) ANN model
    """
    model = MLPClassifier(
        hidden_layer_sizes=tuple(ANN_LAYERS),  # (256, 128, 64)
        activation="relu",                       # ReLU activation
        solver="adam",                            # Adam optimizer
        max_iter=ANN_EPOCHS,                     # Number of training epochs
        batch_size=ANN_BATCH_SIZE,               # Mini-batch size
        random_state=RANDOM_SEED,                # Reproducibility
        early_stopping=True,                     # Early stopping for regularization
        validation_fraction=0.2,                 # 20% validation split
        verbose=True,                            # Show training progress
    )
    return model


def train_ann(X_pca: np.ndarray, cluster_labels: np.ndarray, df) -> tuple:
    """
    Prepare features, create labels, build, and train the ANN model.
    
    Args:
        X_pca: PCA-reduced features
        cluster_labels: K-Means cluster assignments
        df: Original DataFrame (for creating risk labels)
    
    Returns:
        tuple: (trained_model, X_test, y_test, predictions_on_full_data)
    """
    print("=" * 60)
    print("STEP 7: ANN Risk Model Training")
    print("=" * 60)
    
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # --- Prepare input: PCA components + cluster label ---
    X = np.column_stack([X_pca, cluster_labels])
    print(f"  Input shape: {X.shape} (PCA components + cluster label)")
    
    # --- Create proxy risk labels ---
    y = create_risk_label(df)
    print(f"  Risk label distribution: Low Risk={sum(y == 0)}, High Risk={sum(y == 1)}")
    
    # --- Train/Test split ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )
    print(f"  Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    # --- Build and train the model ---
    model = build_ann(input_dim=X.shape[1])
    
    print("\n  Training ANN (MLPClassifier)...")
    model.fit(X_train, y_train)
    
    # --- Save model ---
    joblib.dump(model, ANN_MODEL_PATH)
    print(f"\n  Model saved to: {ANN_MODEL_PATH}")
    
    # --- Predict PD (probability of default) on full dataset ---
    # predict_proba returns [prob_class_0, prob_class_1]
    pd_predictions = model.predict_proba(X)[:, 1]
    print(f"  PD predictions: min={pd_predictions.min():.4f}, max={pd_predictions.max():.4f}, mean={pd_predictions.mean():.4f}")
    print()
    
    return model, X_test, y_test, pd_predictions
