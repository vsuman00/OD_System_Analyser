"""
utils.py - Shared utility functions for the dashboard.
Formatting helpers, color maps, and reusable UI components.
"""

import streamlit as st


def format_pct(value: float, decimals: int = 2) -> str:
    """Format a float as a percentage string."""
    return f"{value * 100:.{decimals}f}%"


def format_currency(value: float) -> str:
    """Format as Indian currency (₹) with commas."""
    if abs(value) >= 1_00_00_000:  # 1 Crore
        return f"₹{value / 1_00_00_000:.2f} Cr"
    elif abs(value) >= 1_00_000:   # 1 Lakh
        return f"₹{value / 1_00_000:.2f} L"
    else:
        return f"₹{value:,.0f}"


def risk_color(pd_value: float) -> str:
    """Return color based on PD risk level."""
    if pd_value < 0.05:
        return "#2ecc71"  # green
    elif pd_value < 0.10:
        return "#3498db"  # blue
    elif pd_value < 0.15:
        return "#f39c12"  # orange
    else:
        return "#e74c3c"  # red


def risk_badge(pd_value: float) -> str:
    """Return a styled badge for risk level."""
    if pd_value < 0.05:
        return "🟢 Very Low"
    elif pd_value < 0.10:
        return "🔵 Low"
    elif pd_value < 0.15:
        return "🟡 Medium"
    else:
        return "🔴 High"


def metric_card(label: str, value: str, delta: str = None):
    """Display a styled metric card using Streamlit."""
    st.metric(label=label, value=value, delta=delta)
