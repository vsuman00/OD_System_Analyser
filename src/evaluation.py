"""
evaluation.py - Model evaluation metrics.
Computes AUC-ROC, classification report, and confusion matrix for the ANN model.
"""

import numpy as np
from sklearn.metrics import (
    roc_auc_score,
    classification_report,
    confusion_matrix,
    accuracy_score,
)


def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    """
    Evaluate the trained ANN model on the test set.
    
    Args:
        model: Trained sklearn MLPClassifier model
        X_test: Test features
        y_test: True test labels
    
    Returns:
        dict: Dictionary containing evaluation metrics
    """
    print("=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)
    
    # --- Generate predictions ---
    y_pred_proba = model.predict_proba(X_test)[:, 1]  # Probability of class 1 (high risk)
    y_pred = model.predict(X_test)                     # Binary labels
    
    # --- Calculate metrics ---
    auc = roc_auc_score(y_test, y_pred_proba)
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["Low Risk", "High Risk"])
    
    # --- Calculate False Negative Rate ---
    # FN = actually high risk but predicted low risk
    if cm.shape == (2, 2):
        fn = cm[1][0]
        tp = cm[1][1]
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
    else:
        fnr = 0.0
    
    # --- Print results ---
    print(f"  AUC-ROC Score      : {auc:.4f}  (Target: > 0.85)")
    print(f"  Accuracy           : {accuracy:.4f}")
    print(f"  False Negative Rate: {fnr:.4f}  (Target: < 0.10)")
    print()
    print("  Confusion Matrix:")
    print(f"    {cm}")
    print()
    print("  Classification Report:")
    print(f"  {report}")
    
    return {
        "auc": auc,
        "accuracy": accuracy,
        "false_negative_rate": fnr,
        "confusion_matrix": cm,
        "classification_report": report,
    }
