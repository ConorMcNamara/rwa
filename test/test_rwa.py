import numpy as np
import pandas as pd

import statsmodels.api as sm

from rwa import johnson_relative_weights


class TestRWA:
    """Test Johnson Relative Weights."""

    @staticmethod
    def test_rwa_results() -> None:
        df = sm.datasets.get_rdataset("mtcars", "datasets", cache=True).data
        mtcars = pd.DataFrame(df)
        weights = johnson_relative_weights(mtcars, ["cyl", "disp", "hp", "gear"], "mpg")
        actual_weight_array = weights.loc["relative weights", :].to_numpy()
        actual_rescaled_array = weights.loc["rescaled relative weights", :].to_numpy()
        # https://martinctc.github.io/rwa/ for comparison
        expected_weight_array = np.array([0.2284797, 0.2221469, 0.2321744, 0.0963886])
        expected_rescaled_array = np.array([29.32274, 28.50999, 29.79691, 12.37037])
        np.testing.assert_allclose(
            actual_weight_array, expected_weight_array, rtol=1e-3
        )
        np.testing.assert_allclose(
            actual_rescaled_array, expected_rescaled_array, rtol=1e-3
        )
