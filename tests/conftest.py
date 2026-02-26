"""Pytest configuration and fixtures for the test suite."""

import pytest


@pytest.fixture(scope="session")
def sample_dataframe():
    """Provide a sample DataFrame for testing.

    Returns
    -------
    pd.DataFrame
        A simple DataFrame with predictors and target variable.
    """
    import pandas as pd

    return pd.DataFrame(
        {
            "x1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "x2": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
            "x3": [1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5, 15.0],
            "y": [2, 5, 8, 11, 14, 17, 20, 23, 26, 29],
        }
    )
