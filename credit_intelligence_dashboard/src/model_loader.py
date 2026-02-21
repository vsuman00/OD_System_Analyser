"""
model_loader.py - Load pre-trained ML models (scaler, PCA, KMeans, ANN).
"""

import joblib
import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import SCALER_PATH, PCA_PATH, KMEANS_PATH, ANN_MODEL_PATH


@st.cache_resource
def load_scaler():
    """Load the fitted StandardScaler."""
    return joblib.load(SCALER_PATH)


@st.cache_resource
def load_pca():
    """Load the fitted PCA model."""
    return joblib.load(PCA_PATH)


@st.cache_resource
def load_kmeans():
    """Load the fitted KMeans model."""
    return joblib.load(KMEANS_PATH)


@st.cache_resource
def load_ann():
    """Load the trained ANN risk model (MLPClassifier)."""
    return joblib.load(ANN_MODEL_PATH)


def load_all_models():
    """Load all models and return as a dict."""
    return {
        "scaler": load_scaler(),
        "pca": load_pca(),
        "kmeans": load_kmeans(),
        "ann": load_ann(),
    }
