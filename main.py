"""
main.py - Entry point for the Intelligent OD Risk & Strategy Optimization System.

This script runs the full ML pipeline:
    Load Data → Clean → Feature Engineering → Scale → PCA → K-Means
    → ANN Risk Model → OD Scoring → Interest Strategy → Sector Report

Usage:
    python main.py
"""

import sys
import os

# Add project root to Python path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.pipeline import run_pipeline


def main():
    """Main entry point - runs the complete pipeline."""
    try:
        results = run_pipeline()
        print("\n✅ System executed successfully!")
        print(f"   Check outputs/ folder for the final strategy report.")
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
