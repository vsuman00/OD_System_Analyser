"""
clustering.py - K-Means clustering for business behavior segmentation.
Segments businesses into 4 groups:
    0: Stable, 1: Growing, 2: Liquidity Stressed, 3: High Risk
The cluster label is used as an additional feature for the ANN model.
"""

import numpy as np
import joblib
from sklearn.cluster import KMeans
from config.config import KMEANS_K, CLUSTER_LABELS, KMEANS_PATH, MODELS_DIR, RANDOM_SEED
import os


def apply_clustering(X_pca: np.ndarray) -> tuple:
    """
    Apply K-Means clustering on PCA-transformed data.
    
    Args:
        X_pca: PCA-reduced feature matrix
    
    Returns:
        tuple: (cluster_labels_array, fitted_kmeans_model)
    """
    print("=" * 60)
    print("STEP 6: K-Means Clustering (K=4)")
    print("=" * 60)
    
    # Create models directory if it doesn't exist
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Fit K-Means
    kmeans = KMeans(n_clusters=KMEANS_K, random_state=RANDOM_SEED, n_init=10)
    cluster_labels = kmeans.fit_predict(X_pca)
    
    # Print cluster distribution
    unique, counts = np.unique(cluster_labels, return_counts=True)
    print("  Cluster distribution:")
    for cluster_id, count in zip(unique, counts):
        label_name = CLUSTER_LABELS.get(cluster_id, f"Cluster {cluster_id}")
        print(f"    Cluster {cluster_id} ({label_name}): {count} businesses")
    
    # Save K-Means model
    joblib.dump(kmeans, KMEANS_PATH)
    print(f"  KMeans model saved to: {KMEANS_PATH}")
    print()
    
    return cluster_labels, kmeans
