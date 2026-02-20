"""
config.py - Central configuration for the Intelligent OD System.
Contains all file paths, feature lists, model hyperparameters, and thresholds.
"""

import os

# ============================================================
# Project root directory (parent of config/)
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# Data paths
# ============================================================
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "1L_real_world_business_financial_stress_dataset.csv")

# ============================================================
# Model save paths
# ============================================================
MODELS_DIR = os.path.join(BASE_DIR, "models")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.pkl")
PCA_PATH = os.path.join(MODELS_DIR, "pca.pkl")
KMEANS_PATH = os.path.join(MODELS_DIR, "kmeans.pkl")
ANN_MODEL_PATH = os.path.join(MODELS_DIR, "ann_risk_model.pkl")

# ============================================================
# Output paths
# ============================================================
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
FINAL_STRATEGY_FILE = os.path.join(OUTPUTS_DIR, "final_od_strategy.csv")

# ============================================================
# Feature columns used from the dataset
# ============================================================
NUMERIC_FEATURES = [
    "Revenue_per_Day",
    "Expense_per_Day",
    "Monthly_Revenue",
    "Monthly_Expense",
    "Cash_Inflow_Adjusted",
    "Cash_Outflow_Adjusted",
    "OD_Required",
    "OD_Utilization",
    "Inventory_Days",
    "Receivable_Days",
    "Payable_Days",
    "Cash_Conversion_Cycle",
    "Credit_Score",
    "Debt_to_Revenue_Ratio",
    "EMI_Obligation",
]

# Engineered feature names (created during feature engineering)
ENGINEERED_FEATURES = [
    "Profit",
    "ProfitMargin",
    "CashRatio",
]

# ============================================================
# PCA settings
# ============================================================
PCA_VARIANCE_THRESHOLD = 0.95  # Retain 95% of variance

# ============================================================
# K-Means settings
# ============================================================
KMEANS_K = 4  # Number of clusters
CLUSTER_LABELS = {
    0: "Stable",
    1: "Growing",
    2: "Liquidity Stressed",
    3: "High Risk",
}

# ============================================================
# ANN (Artificial Neural Network) architecture
# ============================================================
ANN_LAYERS = [256, 128, 64]      # Neuron counts per hidden layer
ANN_DROPOUT = 0.3                 # Dropout rate
ANN_ACTIVATION = "relu"           # Hidden layer activation
ANN_OUTPUT_ACTIVATION = "sigmoid" # Output layer activation
ANN_LOSS = "binary_crossentropy"  # Loss function
ANN_OPTIMIZER = "adam"            # Optimizer
ANN_EPOCHS = 30                   # Training epochs
ANN_BATCH_SIZE = 256              # Batch size
ANN_VALIDATION_SPLIT = 0.2       # Validation split

# ============================================================
# Interest reduction strategy thresholds
# ============================================================
PD_THRESHOLD = 0.15       # Max probability of default for interest reduction
OD_UTIL_THRESHOLD = 0.70  # Min OD utilization for interest reduction

# ============================================================
# Random seed for reproducibility
# ============================================================
RANDOM_SEED = 42
