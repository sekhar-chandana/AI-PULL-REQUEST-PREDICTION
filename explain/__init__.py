"""
==========================================================
AI Pull Request Risk Predictor

Explain Package

This package provides:

1. SHAP explanation generation
2. Groq AI explanation

==========================================================
"""

from .shap_engine import SHAPEngine
from .groq_engine import GroqEngine

__version__ = "1.0.0"

__author__ = "AI Pull Request Risk Predictor"

__all__ = [
    "SHAPEngine",
    "GroqEngine"
]