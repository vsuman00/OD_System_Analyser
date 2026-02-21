"""
styles.py - Glassmorphism CSS theme for the Credit Intelligence Dashboard.
Provides inject_custom_css() that all pages call to apply consistent styling.
"""

import streamlit as st


def inject_custom_css():
    """Inject the full glassmorphism CSS into the current Streamlit page."""
    st.markdown(GLASSMORPHISM_CSS, unsafe_allow_html=True)


GLASSMORPHISM_CSS = """
<style>
/* ═══════════════════════════════════════════════════════
   GOOGLE FONT
   ═══════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif !important;
}

/* ═══════════════════════════════════════════════════════
   MAIN BACKGROUND — Gradient with subtle grain
   ═══════════════════════════════════════════════════════ */
.stApp {
    background: linear-gradient(135deg, #0B0F19 0%, #111827 40%, #0F172A 70%, #1E1B4B 100%) !important;
}

/* ═══════════════════════════════════════════════════════
   SIDEBAR — Glassmorphism
   ═══════════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(99, 102, 241, 0.15) !important;
}

section[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}

section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li,
section[data-testid="stSidebar"] .stMarkdown span {
    color: #CBD5E1 !important;
    font-size: 0.92rem !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] .stCaption p {
    color: #94A3B8 !important;
    font-size: 0.8rem !important;
}

/* Sidebar nav links */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] .stPageLink p {
    color: #A5B4FC !important;
    font-weight: 500 !important;
}

section[data-testid="stSidebar"] a:hover {
    color: #C4B5FD !important;
}

/* ═══════════════════════════════════════════════════════
   METRIC CARDS — Glassmorphism
   ═══════════════════════════════════════════════════════ */
div[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.5) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
}

div[data-testid="stMetric"] label {
    color: #94A3B8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #F1F5F9 !important;
    font-weight: 700 !important;
    font-size: 1.6rem !important;
}

div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
    font-weight: 500 !important;
}

/* ═══════════════════════════════════════════════════════
   HEADINGS
   ═══════════════════════════════════════════════════════ */
h1 {
    color: #F8FAFC !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
    background: linear-gradient(135deg, #A5B4FC, #818CF8, #6366F1) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

h2, h3 {
    color: #E2E8F0 !important;
    font-weight: 700 !important;
}

h2::after {
    content: '';
    display: block;
    width: 50px;
    height: 3px;
    background: linear-gradient(to right, #6366F1, transparent);
    margin-top: 6px;
    border-radius: 3px;
}

/* ═══════════════════════════════════════════════════════
   BODY TEXT
   ═══════════════════════════════════════════════════════ */
.stMarkdown p, .stMarkdown li {
    color: #CBD5E1 !important;
    line-height: 1.7 !important;
}

.stMarkdown strong {
    color: #F1F5F9 !important;
}

hr {
    border-color: rgba(99, 102, 241, 0.15) !important;
    margin: 1.5rem 0 !important;
}

/* ═══════════════════════════════════════════════════════
   DATAFRAMES / TABLES — Glassmorphism
   ═══════════════════════════════════════════════════════ */
div[data-testid="stDataFrame"],
.stDataFrame {
    background: rgba(30, 41, 59, 0.4) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(99, 102, 241, 0.15) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Markdown tables */
table {
    background: rgba(30, 41, 59, 0.4) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

th {
    background: rgba(99, 102, 241, 0.15) !important;
    color: #E2E8F0 !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
    border-bottom: 1px solid rgba(99, 102, 241, 0.2) !important;
}

td {
    color: #CBD5E1 !important;
    padding: 10px 16px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
}

tr:hover td {
    background: rgba(99, 102, 241, 0.08) !important;
}

/* ═══════════════════════════════════════════════════════
   PLOTLY CHARTS — Glass container
   ═══════════════════════════════════════════════════════ */
div[data-testid="stPlotlyChart"] {
    background: rgba(30, 41, 59, 0.35) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(99, 102, 241, 0.12) !important;
    border-radius: 16px !important;
    padding: 8px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
}

/* ═══════════════════════════════════════════════════════
   INFO / WARNING / SUCCESS BOXES
   ═══════════════════════════════════════════════════════ */
div[data-testid="stAlert"] {
    background: rgba(30, 41, 59, 0.5) !important;
    backdrop-filter: blur(12px) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
}

.stAlert p {
    color: #E2E8F0 !important;
}

/* ═══════════════════════════════════════════════════════
   INPUTS / SLIDERS / SELECT BOXES
   ═══════════════════════════════════════════════════════ */
.stSlider > div > div {
    background: rgba(99, 102, 241, 0.3) !important;
}

div[data-testid="stSliderTickBarMin"],
div[data-testid="stSliderTickBarMax"] {
    color: #94A3B8 !important;
}

.stTextInput > div > div > input {
    background: rgba(30, 41, 59, 0.6) !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
    color: #F1F5F9 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
}

.stSelectbox > div > div {
    background: rgba(30, 41, 59, 0.6) !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
    border-radius: 10px !important;
}

/* ═══════════════════════════════════════════════════════
   EXPANDER
   ═══════════════════════════════════════════════════════ */
details {
    background: rgba(30, 41, 59, 0.4) !important;
    border: 1px solid rgba(99, 102, 241, 0.15) !important;
    border-radius: 12px !important;
}

details summary {
    color: #E2E8F0 !important;
    font-weight: 600 !important;
}

/* ═══════════════════════════════════════════════════════
   TABS
   ═══════════════════════════════════════════════════════ */
button[data-baseweb="tab"] {
    color: #94A3B8 !important;
    font-weight: 500 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #A5B4FC !important;
    border-bottom-color: #6366F1 !important;
}

/* ═══════════════════════════════════════════════════════
   SCROLLBAR
   ═══════════════════════════════════════════════════════ */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.5);
}

::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.3);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.5);
}
</style>
"""
