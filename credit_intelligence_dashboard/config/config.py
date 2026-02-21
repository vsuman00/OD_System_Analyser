"""
config.py - Configuration for the Credit Intelligence Dashboard.
Points to ML pipeline outputs (models, data, strategy CSV).
"""

import os

# ============================================================
# Paths — relative to the dashboard root
# ============================================================
DASHBOARD_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(DASHBOARD_DIR)  # intelligent_od_system/

# Data from ML pipeline
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "1L_real_world_business_financial_stress_dataset.csv")
STRATEGY_CSV_PATH = os.path.join(DASHBOARD_DIR, "data", "final_od_strategy.csv")

# Saved models from ML pipeline
MODELS_DIR = os.path.join(DASHBOARD_DIR, "models")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.pkl")
PCA_PATH = os.path.join(MODELS_DIR, "pca.pkl")
KMEANS_PATH = os.path.join(MODELS_DIR, "kmeans.pkl")
ANN_MODEL_PATH = os.path.join(MODELS_DIR, "ann_risk_model.pkl")

# Outputs
OUTPUTS_DIR = os.path.join(DASHBOARD_DIR, "outputs")

# ============================================================
# Cluster labels
# ============================================================
CLUSTER_LABELS = {
    0: "Stable",
    1: "Growing",
    2: "Liquidity Stressed",
    3: "High Risk",
}

# Cluster colors for consistent styling
CLUSTER_COLORS = {
    "Stable": "#2ecc71",
    "Growing": "#3498db",
    "Liquidity Stressed": "#f39c12",
    "High Risk": "#e74c3c",
}

# Risk thresholds
PD_THRESHOLD = 0.15
OD_UTIL_THRESHOLD = 0.70

# Feature lists
NUMERIC_FEATURES = [
    "Revenue_per_Day", "Expense_per_Day", "Monthly_Revenue", "Monthly_Expense",
    "Cash_Inflow_Adjusted", "Cash_Outflow_Adjusted", "OD_Required", "OD_Utilization",
    "Inventory_Days", "Receivable_Days", "Payable_Days", "Cash_Conversion_Cycle",
    "Credit_Score", "Debt_to_Revenue_Ratio", "EMI_Obligation",
]
ENGINEERED_FEATURES = ["Profit", "ProfitMargin", "CashRatio"]
