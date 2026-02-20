"""
visualization.py - PCA & KMeans Visualization Module.

Provides 5 professional visualization functions:
    1. plot_explained_variance  - PCA explained variance per component
    2. plot_cumulative_variance - Cumulative variance with 95% threshold line
    3. plot_pca_3d              - 3D PCA projection scatter plot
    4. plot_clusters_3d         - 3D PCA scatter colored by KMeans clusters
    5. plot_elbow_curve         - Elbow method for optimal K selection

Technical constraints:
    - Uses ONLY matplotlib and numpy (no seaborn)
    - Each visualization is a separate figure (no subplots)
    - Efficient for 100K rows
    - All functions are modular and reusable
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for saving plots
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D projection)
from sklearn.cluster import KMeans
import os

from config.config import OUTPUTS_DIR


# ============================================================
# Helper: Save figure to outputs directory
# ============================================================
def _save_fig(fig, filename: str):
    """Save figure to the outputs directory and close it."""
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUTS_DIR, filename)
    fig.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"    Saved: {filepath}")


# ============================================================
# 1. Explained Variance Plot
# ============================================================
def plot_explained_variance(pca):
    """
    Bar plot of PCA explained variance ratio per component.
    
    Shows how much variance each principal component captures,
    justifying PCA usage and component selection.
    
    Args:
        pca: Fitted sklearn PCA model
    """
    n_components = len(pca.explained_variance_ratio_)
    components = np.arange(1, n_components + 1)
    variance = pca.explained_variance_ratio_

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar chart with gradient-like coloring
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, n_components))
    bars = ax.bar(components, variance, color=colors, edgecolor="black", linewidth=0.5)
    
    # Add value labels on top of each bar
    for bar, val in zip(bars, variance):
        ax.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002,
            f"{val:.3f}", ha="center", va="bottom", fontsize=9, fontweight="bold"
        )
    
    # Styling
    ax.set_xlabel("Principal Component", fontsize=12, fontweight="bold")
    ax.set_ylabel("Explained Variance Ratio", fontsize=12, fontweight="bold")
    ax.set_title("PCA Explained Variance Ratio", fontsize=14, fontweight="bold")
    ax.set_xticks(components)
    ax.set_xticklabels([f"PC{i}" for i in components], rotation=45)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.set_ylim(0, max(variance) * 1.2)
    
    _save_fig(fig, "pca_explained_variance.png")


# ============================================================
# 2. Cumulative Explained Variance
# ============================================================
def plot_cumulative_variance(pca):
    """
    Line plot of cumulative explained variance with 95% threshold.
    
    Shows how many components are needed to capture 95% of the
    total variance in the data.
    
    Args:
        pca: Fitted sklearn PCA model
    """
    cumulative = np.cumsum(pca.explained_variance_ratio_)
    n_components = len(cumulative)
    components = np.arange(1, n_components + 1)

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Cumulative variance line
    ax.plot(
        components, cumulative, "o-",
        color="#2196F3", linewidth=2.5, markersize=8,
        markerfacecolor="white", markeredgewidth=2, label="Cumulative Variance"
    )
    
    # Fill under the curve
    ax.fill_between(components, cumulative, alpha=0.15, color="#2196F3")
    
    # 95% threshold line
    ax.axhline(y=0.95, color="#E53935", linewidth=2, linestyle="--", label="95% Threshold")
    
    # Mark the component where 95% is first reached
    idx_95 = np.argmax(cumulative >= 0.95)
    if cumulative[idx_95] >= 0.95:
        ax.scatter(
            [components[idx_95]], [cumulative[idx_95]],
            color="#E53935", s=150, zorder=5, edgecolors="black", linewidth=1.5
        )
        ax.annotate(
            f"PC{components[idx_95]}: {cumulative[idx_95]:.3f}",
            xy=(components[idx_95], cumulative[idx_95]),
            xytext=(components[idx_95] + 0.5, cumulative[idx_95] - 0.06),
            fontsize=10, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
        )
    
    # Styling
    ax.set_xlabel("Number of Components", fontsize=12, fontweight="bold")
    ax.set_ylabel("Cumulative Explained Variance", fontsize=12, fontweight="bold")
    ax.set_title("Cumulative Explained Variance", fontsize=14, fontweight="bold")
    ax.set_xticks(components)
    ax.set_xticklabels([f"PC{i}" for i in components])
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=11, loc="lower right")
    ax.grid(alpha=0.3, linestyle="--")
    
    _save_fig(fig, "pca_cumulative_variance.png")


# ============================================================
# 3. 3D PCA Projection
# ============================================================
def plot_pca_3d(Z: np.ndarray):
    """
    3D scatter plot of the first three PCA components.
    
    Visualizes the data distribution in reduced 3D space.
    For 100K rows, uses smaller marker size and alpha for clarity.
    
    Args:
        Z: PCA-transformed matrix (n_samples, n_components), uses first 3
    """
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection="3d")
    
    # Subsample for performance if dataset is very large (>50K)
    n = Z.shape[0]
    if n > 50000:
        idx = np.random.choice(n, size=50000, replace=False)
        Z_plot = Z[idx]
    else:
        Z_plot = Z
    
    # 3D scatter plot
    scatter = ax.scatter(
        Z_plot[:, 0], Z_plot[:, 1], Z_plot[:, 2],
        c=Z_plot[:, 0],         # Color by PC1 value for depth perception
        cmap="coolwarm",
        s=2, alpha=0.4,         # Small markers, semi-transparent for 100K data
        edgecolors="none"
    )
    
    # Labels and title
    ax.set_xlabel("PC1", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_ylabel("PC2", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_zlabel("PC3", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_title("3D PCA Projection", fontsize=14, fontweight="bold", pad=20)
    
    # Add colorbar
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=20, pad=0.1)
    cbar.set_label("PC1 Value", fontsize=10)
    
    # Set viewing angle for better perspective
    ax.view_init(elev=25, azim=45)
    
    _save_fig(fig, "pca_3d_projection.png")


# ============================================================
# 4. 3D PCA with KMeans Clusters
# ============================================================
def plot_clusters_3d(Z: np.ndarray, cluster_labels: np.ndarray):
    """
    3D scatter plot colored by KMeans cluster assignments.
    Marks cluster centroids in 3D space.
    
    Does NOT hardcode number of clusters — dynamically detects from labels.
    
    Args:
        Z: PCA-transformed matrix (n_samples, n_components), uses first 3
        cluster_labels: Array of cluster assignments (one per sample)
    """
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection="3d")
    
    # Get unique clusters (not hardcoded)
    unique_clusters = np.unique(cluster_labels)
    n_clusters = len(unique_clusters)
    
    # Color map for clusters
    colors = plt.cm.Set1(np.linspace(0, 1, max(n_clusters, 3)))
    
    # Cluster name mapping (from config if available)
    try:
        from config.config import CLUSTER_LABELS as cluster_name_map
    except ImportError:
        cluster_name_map = {}
    
    # Subsample for performance if dataset is very large
    n = Z.shape[0]
    if n > 50000:
        idx = np.random.choice(n, size=50000, replace=False)
        Z_plot = Z[idx]
        labels_plot = cluster_labels[idx]
    else:
        Z_plot = Z
        labels_plot = cluster_labels
    
    # Plot each cluster separately for legend
    for i, cluster_id in enumerate(unique_clusters):
        mask = labels_plot == cluster_id
        label_name = cluster_name_map.get(cluster_id, f"Cluster {cluster_id}")
        ax.scatter(
            Z_plot[mask, 0], Z_plot[mask, 1], Z_plot[mask, 2],
            c=[colors[i]], s=3, alpha=0.4, label=label_name,
            edgecolors="none"
        )
    
    # Compute and plot centroids using FULL data (not subsampled)
    for i, cluster_id in enumerate(unique_clusters):
        mask_full = cluster_labels == cluster_id
        centroid = Z[mask_full, :3].mean(axis=0)
        ax.scatter(
            [centroid[0]], [centroid[1]], [centroid[2]],
            c="black", s=200, marker="X", edgecolors="white", linewidth=2,
            zorder=10
        )
    
    # Labels and title
    ax.set_xlabel("PC1", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_ylabel("PC2", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_zlabel("PC3", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_title("3D PCA Clusters", fontsize=14, fontweight="bold", pad=20)
    ax.legend(fontsize=10, loc="upper right", markerscale=5)
    
    # Set viewing angle
    ax.view_init(elev=25, azim=45)
    
    _save_fig(fig, "pca_3d_clusters.png")


# ============================================================
# 5. Elbow Method Plot
# ============================================================
def plot_elbow_curve(X_scaled: np.ndarray, max_k: int = 10):
    """
    Plot the Elbow Method curve to help determine optimal K for KMeans.
    
    Computes inertia (within-cluster sum of squares) for k=1 to max_k
    and plots the curve. The 'elbow' point suggests the optimal K.
    
    Args:
        X_scaled: Scaled feature matrix (or PCA-reduced matrix)
        max_k: Maximum number of clusters to evaluate (default: 10)
    """
    # Subsample for speed if dataset is very large
    n = X_scaled.shape[0]
    if n > 30000:
        idx = np.random.choice(n, size=30000, replace=False)
        X_sample = X_scaled[idx]
    else:
        X_sample = X_scaled
    
    # Compute inertia for each K
    k_range = range(1, max_k + 1)
    inertias = []
    print("    Computing elbow curve...")
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_sample)
        inertias.append(kmeans.inertia_)
        print(f"      K={k}: inertia={kmeans.inertia_:.0f}")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the elbow curve
    ax.plot(
        list(k_range), inertias, "o-",
        color="#FF6F00", linewidth=2.5, markersize=10,
        markerfacecolor="white", markeredgewidth=2, markeredgecolor="#FF6F00"
    )
    
    # Highlight the chosen K=4 (from PRD)
    if 4 <= max_k:
        ax.scatter(
            [4], [inertias[3]], color="#E53935", s=200,
            zorder=5, edgecolors="black", linewidth=2
        )
        ax.annotate(
            f"K=4 (Selected)", xy=(4, inertias[3]),
            xytext=(5, inertias[3] + (inertias[0] - inertias[-1]) * 0.1),
            fontsize=11, fontweight="bold", color="#E53935",
            arrowprops=dict(arrowstyle="->", color="#E53935", lw=2),
        )
    
    # Styling
    ax.set_xlabel("Number of Clusters (K)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Inertia (WCSS)", fontsize=12, fontweight="bold")
    ax.set_title("Elbow Method for Optimal K", fontsize=14, fontweight="bold")
    ax.set_xticks(list(k_range))
    ax.grid(alpha=0.3, linestyle="--")
    
    _save_fig(fig, "elbow_curve.png")


# ============================================================
# Run All Visualizations
# ============================================================
def generate_all_visualizations(pca, X_pca, cluster_labels, X_scaled):
    """
    Generate all 5 visualizations in one call.
    
    Args:
        pca: Fitted PCA model
        X_pca: PCA-transformed matrix
        cluster_labels: KMeans cluster assignments
        X_scaled: Scaled feature matrix (for elbow curve)
    """
    print("=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)
    
    print("  [1/5] Explained Variance Plot...")
    plot_explained_variance(pca)
    
    print("  [2/5] Cumulative Variance Plot...")
    plot_cumulative_variance(pca)
    
    print("  [3/5] 3D PCA Projection...")
    plot_pca_3d(X_pca)
    
    print("  [4/5] 3D PCA Clusters...")
    plot_clusters_3d(X_pca, cluster_labels)
    
    print("  [5/5] Elbow Curve...")
    plot_elbow_curve(X_scaled, max_k=10)
    
    print("\n  All visualizations saved to outputs/ folder")
    print()
