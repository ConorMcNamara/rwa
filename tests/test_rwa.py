"""Tests for Johnson Relative Weights Analysis."""

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm

from rwa import johnson_relative_weights


class TestRWA:
    """Test Johnson Relative Weights."""

    @staticmethod
    def test_rwa_results() -> None:
        """Test that RWA produces expected results with realistic data."""
        # Create a dataset with known relationships
        np.random.seed(42)
        n = 50
        x1 = np.random.randn(n)
        x2 = np.random.randn(n)
        x3 = np.random.randn(n)

        # Create y with known weights: y = 2*x1 + 1*x2 + 0.5*x3 + noise
        y = 2 * x1 + 1 * x2 + 0.5 * x3 + 0.5 * np.random.randn(n)

        df = pd.DataFrame({"x1": x1, "x2": x2, "x3": x3, "y": y})

        weights = johnson_relative_weights(df, ["x1", "x2", "x3"], "y")

        # Check that weights sum to approximately 100
        rescaled_sum = weights.loc[:, "rescaled relative weights"].sum()
        assert np.abs(rescaled_sum - 100.0) < 0.1

        # Check that all weights are positive
        assert all(weights.loc[:, "relative weights"] >= 0)
        assert all(weights.loc[:, "rescaled relative weights"] >= 0)

        # Check that x1 has the highest weight (it has the strongest effect)
        assert weights.loc["x1", "relative weights"] == weights.loc[:, "relative weights"].max()

    @staticmethod
    def test_invalid_dataframe() -> None:
        """Test that TypeError is raised for non-DataFrame input."""
        with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
            johnson_relative_weights([1, 2, 3], x_vars=["x1"], y_var="y")

    @staticmethod
    def test_missing_variables() -> None:
        """Test that ValueError is raised when both x_vars and y_var are missing."""
        df = pd.DataFrame({"x1": [1, 2, 3], "y": [1, 2, 3]})
        with pytest.raises(ValueError, match="y_var must be provided"):
            johnson_relative_weights(df)

    @staticmethod
    def test_infer_y_var() -> None:
        """Test that y_var can be inferred from x_vars."""
        np.random.seed(42)
        df = pd.DataFrame(
            {
                "x1": np.random.randn(20),
                "x2": np.random.randn(20),
                "y": np.random.randn(20),
            }
        )
        weights = johnson_relative_weights(df, x_vars=["x1", "x2"])
        assert weights is not None
        assert len(weights) == 2
        assert list(weights.index) == ["x1", "x2"]

    @staticmethod
    def test_infer_x_vars() -> None:
        """Test that x_vars can be inferred from y_var."""
        np.random.seed(42)
        df = pd.DataFrame(
            {
                "x1": np.random.randn(20),
                "x2": np.random.randn(20),
                "y": np.random.randn(20),
            }
        )
        weights = johnson_relative_weights(df, y_var="y")
        assert weights is not None
        assert len(weights) == 2
        assert set(weights.index) == {"x1", "x2"}

    @staticmethod
    def test_output_structure() -> None:
        """Test that output DataFrame has correct structure."""
        np.random.seed(42)
        df = pd.DataFrame(
            {
                "x1": np.random.randn(30),
                "x2": np.random.randn(30),
                "x3": np.random.randn(30),
                "y": np.random.randn(30),
            }
        )
        weights = johnson_relative_weights(df, ["x1", "x2", "x3"], "y")

        assert isinstance(weights, pd.DataFrame)
        assert list(weights.columns) == ["relative weights", "rescaled relative weights"]
        assert len(weights) == 3
        assert all(weights.index == ["x1", "x2", "x3"])

    @staticmethod
    def test_rescaled_weights_sum_to_100() -> None:
        """Test that rescaled weights always sum to 100."""
        np.random.seed(123)
        for _ in range(5):
            df = pd.DataFrame(
                {
                    "x1": np.random.randn(25),
                    "x2": np.random.randn(25),
                    "x3": np.random.randn(25),
                    "y": np.random.randn(25),
                }
            )
            weights = johnson_relative_weights(df, ["x1", "x2", "x3"], "y")
            rescaled_sum = weights.loc[:, "rescaled relative weights"].sum()
            assert np.abs(rescaled_sum - 100.0) < 0.1

    @staticmethod
    def test_output_is_real_valued() -> None:
        """Test that weights are real floats, not complex.

        The correlation matrix is symmetric, so eigh is used instead of eig. Using
        eig produced a complex dtype that leaked into the returned weights.
        """
        np.random.seed(42)
        df = pd.DataFrame(
            {
                "x1": np.random.randn(30),
                "x2": np.random.randn(30),
                "y": np.random.randn(30),
            }
        )
        weights = johnson_relative_weights(df, ["x1", "x2"], "y")

        for column in weights.columns:
            assert weights[column].dtype == np.float64
            assert not np.iscomplexobj(weights[column].to_numpy())

    @staticmethod
    def test_perfect_collinearity_raises() -> None:
        """Test that perfectly collinear predictors raise an informative error."""
        df = pd.DataFrame({"x1": [1, 2, 3, 4, 5], "x2": [2, 4, 6, 8, 10], "y": [1, 3, 5, 7, 9]})
        with pytest.raises(ValueError, match="collinear"):
            johnson_relative_weights(df, x_vars=["x1", "x2"], y_var="y")

    @staticmethod
    def test_zero_variance_y_raises() -> None:
        """Test that constant y_var raises an informative error."""
        np.random.seed(42)
        df = pd.DataFrame(
            {
                "x1": np.random.randn(20),
                "x2": np.random.randn(20),
                "y": np.full(20, 5.0),
            }
        )
        with pytest.raises(ValueError, match="zero variance"):
            johnson_relative_weights(df, x_vars=["x1", "x2"], y_var="y")

    @staticmethod
    def test_zero_variance_x_raises() -> None:
        """Test that a constant predictor raises an informative error."""
        np.random.seed(42)
        df = pd.DataFrame(
            {
                "x1": np.random.randn(20),
                "x2": np.full(20, 3.0),
                "y": np.random.randn(20),
            }
        )
        with pytest.raises(ValueError, match="zero variance"):
            johnson_relative_weights(df, x_vars=["x1", "x2"], y_var="y")

    @staticmethod
    def test_zero_r_squared_raises() -> None:
        """Test that predictors orthogonal to y_var raise an informative error."""
        df = pd.DataFrame(
            {
                "x1": [1, -1, 1, -1],
                "x2": [1, 1, -1, -1],
                "y": [1, -1, -1, 1],
            }
        )
        with pytest.raises(ValueError, match="R-squared is zero"):
            johnson_relative_weights(df, x_vars=["x1", "x2"], y_var="y")

    @staticmethod
    def test_apply_signs_output_structure() -> None:
        """Test that apply_signs adds the signed rescaled column."""
        np.random.seed(42)
        n = 50
        x1 = np.random.randn(n)
        x2 = np.random.randn(n)
        y = 2 * x1 - 1 * x2 + 0.5 * np.random.randn(n)
        df = pd.DataFrame({"x1": x1, "x2": x2, "y": y})

        weights = johnson_relative_weights(df, ["x1", "x2"], "y", apply_signs=True)
        assert "signed rescaled relative weights" in weights.columns
        assert len(weights.columns) == 3

    @staticmethod
    def test_apply_signs_values() -> None:
        """Test that signed weights have correct signs and magnitudes."""
        np.random.seed(42)
        n = 200
        x1 = np.random.randn(n)
        x2 = np.random.randn(n)
        y = 3 * x1 - 2 * x2 + 0.3 * np.random.randn(n)
        df = pd.DataFrame({"x1": x1, "x2": x2, "y": y})

        weights = johnson_relative_weights(df, ["x1", "x2"], "y", apply_signs=True)
        signed = weights["signed rescaled relative weights"]
        rescaled = weights["rescaled relative weights"]
        assert signed["x1"] > 0
        assert signed["x2"] < 0
        np.testing.assert_allclose(np.abs(signed).to_numpy(), rescaled.to_numpy())

    @staticmethod
    def test_apply_signs_false_excludes_column() -> None:
        """Test that signed column is absent when apply_signs is False."""
        np.random.seed(42)
        df = pd.DataFrame(
            {"x1": np.random.randn(20), "x2": np.random.randn(20), "y": np.random.randn(20)}
        )
        weights = johnson_relative_weights(df, ["x1", "x2"], "y", apply_signs=False)
        assert "signed rescaled relative weights" not in weights.columns

    @staticmethod
    def test_sample_fixture_works(sample_dataframe: pd.DataFrame) -> None:
        """Test that the shared fixture produces valid results."""
        weights = johnson_relative_weights(sample_dataframe, y_var="y")
        assert weights is not None
        assert all(weights["relative weights"] >= 0)

    @staticmethod
    @pytest.mark.network
    def test_rwa_toy_dataset() -> None:
        """Tests rwa on a known toy dataset (requires network access)."""
        try:
            df = sm.datasets.get_rdataset("mtcars", "datasets", cache=True).data
        except Exception as e:
            pytest.skip(f"Could not download mtcars dataset: {e}")

        mtcars = pd.DataFrame(df)
        weights = johnson_relative_weights(mtcars, ["cyl", "disp", "hp", "gear"], "mpg")
        actual_weight_array = weights.loc[:, "relative weights"].to_numpy()
        actual_rescaled_array = weights.loc[:, "rescaled relative weights"].to_numpy()
        # https://martinctc.github.io/rwa/ for comparison
        expected_weight_array = np.array([0.2284797, 0.2221469, 0.2321744, 0.0963886])
        expected_rescaled_array = np.array([29.32274, 28.50999, 29.79691, 12.37037])
        np.testing.assert_allclose(actual_weight_array, expected_weight_array, rtol=1e-6)
        np.testing.assert_allclose(actual_rescaled_array, expected_rescaled_array, rtol=1e-6)


if __name__ == "__main__":
    pytest.main([__file__])
