"""Johnson's Relative Weights Analysis for Regression.

This package provides functionality to calculate Johnson's Relative Weights
for regression analysis, helping determine which variables contribute most
to R-squared.
"""

from rwa.core import johnson_relative_weights

__version__ = "1.0.0"
__all__ = ["johnson_relative_weights"]
