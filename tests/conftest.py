"""Pytest configuration and fixtures for the test suite."""

import pandas as pd
import pytest


@pytest.fixture(scope="session")
def sample_dataframe() -> pd.DataFrame:
    """Provide a sample DataFrame for testing.

    Returns
    -------
    pd.DataFrame
        A simple DataFrame with predictors and target variable.
    """
    return pd.DataFrame(
        {
            "x1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "x2": [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
            "x3": [2, 7, 1, 8, 2, 8, 1, 8, 2, 8],
            "y": [2, 5, 8, 11, 14, 17, 20, 23, 26, 29],
        }
    )
