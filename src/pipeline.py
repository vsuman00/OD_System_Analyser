"""
pipeline.py - End-to-end ML pipeline orchestrator.

Flow (per PRD):
    Load Data → Clean Data → Feature Engineering → Scaling
    → PCA → K-Means → ANN Risk Model → Predict PD
    → Compute ODScore → Apply Interest Strategy
    → Aggregate by Business Type → Generate Final Strategy Report
"""

import sys
import os
import numpy as np

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import NUMERIC_FEATURES, ENGINEERED_FEATURES, CLUSTER_LABELS
from src.data_loader import load_data
from src.preprocessing import preprocess_data
from src.feature_engineering import engineer_features
from src.scaling import scale_features
from src.pca_module import apply_pca
from src.clustering import apply_clustering
from src.ann_risk_model import train_ann
from src.od_scoring import compute_od_score
from src.interest_strategy import apply_interest_strategy
from src.sector_analysis import analyze_sectors
from src.evaluation import evaluate_model
from src.visualization import generate_all_visualizations


def run_pipeline():
    """
    Execute the full Intelligent OD System pipeline.
    
    Returns:
        dict: Summary of results including sector report and evaluation metrics
    """
    print("\n" + "=" * 60)
    print("  INTELLIGENT OD RISK & STRATEGY OPTIMIZATION SYSTEM")
    print("  PCA + K-Means + ANN Pipeline")
    print("=" * 60 + "\n")
    
    # -----------------------------------------------------------
    # STEP 1: Load Data
    # -----------------------------------------------------------
    df = load_data()
    
    # -----------------------------------------------------------
    # STEP 2: Preprocess / Clean Data
    # -----------------------------------------------------------
    df = preprocess_data(df)
    
    # -----------------------------------------------------------
    # STEP 3: Feature Engineering
    # -----------------------------------------------------------
    df = engineer_features(df)
    
    # -----------------------------------------------------------
    # STEP 4: Scale Features
    # Combine original numeric features + engineered features
    # -----------------------------------------------------------
    feature_cols = NUMERIC_FEATURES + ENGINEERED_FEATURES
    X_scaled, scaler = scale_features(df, feature_cols)
    
    # -----------------------------------------------------------
    # STEP 5: PCA (Dimensionality Reduction)
    # -----------------------------------------------------------
    X_pca, pca = apply_pca(X_scaled)
    
    # -----------------------------------------------------------
    # STEP 6: K-Means Clustering
    # -----------------------------------------------------------
    cluster_labels, kmeans = apply_clustering(X_pca)
    
    # Add cluster labels to the DataFrame
    df["Cluster"] = cluster_labels
    df["Cluster_Name"] = df["Cluster"].map(CLUSTER_LABELS)
    
    # -----------------------------------------------------------
    # STEP 7: ANN Risk Model (Train + Predict PD)
    # -----------------------------------------------------------
    model, X_test, y_test, pd_predictions = train_ann(X_pca, cluster_labels, df)
    
    # -----------------------------------------------------------
    # STEP 8: OD Suitability Scoring
    # -----------------------------------------------------------
    df = compute_od_score(df, pd_predictions)
    
    # -----------------------------------------------------------
    # STEP 9: Interest Reduction Strategy
    # -----------------------------------------------------------
    df = apply_interest_strategy(df)
    
    # -----------------------------------------------------------
    # STEP 10: Sector Analysis & Report Generation
    # -----------------------------------------------------------
    sector_report = analyze_sectors(df)
    
    # -----------------------------------------------------------
    # MODEL EVALUATION
    # -----------------------------------------------------------
    metrics = evaluate_model(model, X_test, y_test)
    
    # -----------------------------------------------------------
    # VISUALIZATIONS (PCA + KMeans plots)
    # -----------------------------------------------------------
    generate_all_visualizations(pca, X_pca, cluster_labels, X_scaled)
    
    # -----------------------------------------------------------
    # FINAL SUMMARY
    # -----------------------------------------------------------
    print("=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)
    print(f"  Total businesses processed : {len(df)}")
    print(f"  Business types analyzed    : {df['Business_Type'].nunique()}")
    print(f"  AUC-ROC Score              : {metrics['auc']:.4f}")
    print(f"  False Negative Rate        : {metrics['false_negative_rate']:.4f}")
    print(f"  Interest reduction eligible: {df['Interest_Reduction'].sum()}")
    print("=" * 60)
    
    return {
        "dataframe": df,
        "sector_report": sector_report,
        "metrics": metrics,
        "model": model,
    }
