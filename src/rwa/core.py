"""Core functionality for Johnson's Relative Weights Analysis."""

import numpy as np
import pandas as pd


def johnson_relative_weights(
    df: pd.DataFrame,
    x_vars: list[str] | None = None,
    y_var: str | None = None,
    plot_weights: bool = False,
    plot_rescaled: bool = False,
) -> pd.DataFrame:
    """Calculate Johnson's Relative Weights for Regression results.

    This helps determine the variables that contribute the most to R-squared.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data
    x_vars : list[str], optional
        A list containing all X variables for the regression.
        Optional if y_var is provided.
    y_var : str, optional
        The y-variable metric. Optional if x_vars is provided.
    plot_weights : bool, default=False
        Whether to plot the relative weights
    plot_rescaled : bool, default=False
        Whether to plot the rescaled relative weights

    Returns
    -------
    pd.DataFrame
        The Johnson's relative weights for each variable in X,
        as well as the rescaled weights

    Raises
    ------
    TypeError
        If df is not a pandas DataFrame
    ValueError
        If neither y_var nor x_vars are provided, if y_var has zero
        variance, if the predictors in x_vars are perfectly collinear,
        or if R-squared is zero
    ImportError
        If plotting is requested but Plotly is not installed

    Notes
    -----
    Johnson's Relative Weights is a technique used in regression analysis
    to determine which variables contribute the most to r-squared.

    References
    ----------
    .. [1] https://www.statisticshowto.com/relative-weights/

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'x1': [1, 2, 3, 4, 5],
    ...     'x2': [5, 3, 4, 1, 2],
    ...     'y': [3, 5, 7, 10, 14]
    ... })
    >>> weights = johnson_relative_weights(df, x_vars=['x1', 'x2'], y_var='y')
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    if y_var is None:
        if x_vars is not None:
            y_var_series = df.columns.difference(x_vars)
            if len(y_var_series) != 1:
                raise ValueError("Could not determine a single y_var from x_vars")
            y_var = y_var_series[0]
        else:
            raise ValueError("y_var must be provided")

    if x_vars is None:
        if y_var is not None:
            x_vars = list(df.columns.difference([y_var]))
        else:
            raise ValueError("x_vars must be provided")

    # Create a subset DataFrame with only the relevant columns
    new_df = df[[y_var] + x_vars]

    # Calculate correlation matrix
    correlation_matrix = new_df.corr()

    # Extract correlations
    y_corr = correlation_matrix[y_var].drop(y_var, axis=0)
    if y_corr.isna().any():
        raise ValueError(
            "y_var has zero variance, so correlations with the predictors "
            "are undefined and relative weights cannot be computed."
        )
    x_corr = correlation_matrix[x_vars].drop(y_var, axis=0)

    # Eigenvalue decomposition. The correlation matrix is real and symmetric, so
    # eigh is used rather than eig: it guarantees real eigenvalues and orthonormal
    # eigenvectors, whereas eig returns complex dtype that propagates all the way
    # into the returned weights.
    eig_val, eig_vec = np.linalg.eigh(x_corr)

    # A correlation matrix is positive semi-definite, so any negative eigenvalue is
    # floating-point noise. Clip to zero, then check for effective singularity
    # before proceeding.
    eig_val = np.clip(eig_val, 0.0, None)
    tol = eig_val.max() * len(eig_val) * np.finfo(float).eps
    if eig_val.min() < tol:
        raise ValueError(
            "The predictors in x_vars are perfectly (or near-perfectly) collinear, "
            "so their correlation matrix is singular and relative weights cannot be "
            "computed. Drop redundant predictors and try again."
        )

    diag_eig = np.diagflat(eig_val)
    sqrt_diag_eig_val = np.sqrt(diag_eig)
    eigen_vec_t = eig_vec.T

    # Calculate lambda matrix
    lamda = np.matmul(np.matmul(eig_vec, sqrt_diag_eig_val), eigen_vec_t)
    inv_lamda = np.linalg.inv(lamda)
    lamda_squared = np.square(lamda)

    # Calculate partial effects and weights
    partial_effect = np.matmul(inv_lamda, y_corr)
    r_squared = np.sum(np.square(partial_effect))
    if r_squared < np.finfo(float).eps:
        raise ValueError(
            "R-squared is zero (or numerically indistinguishable from zero) — "
            "the predictors have no linear relationship with y_var, so "
            "relative weights are undefined."
        )
    raw_relative_weight = np.matmul(lamda_squared, np.square(partial_effect))

    # Create results DataFrame
    weights = pd.DataFrame(
        np.array([raw_relative_weight, raw_relative_weight * 100 / r_squared]).reshape(2, len(x_vars)),
        columns=x_vars,
    )
    weights.index = ["relative weights", "rescaled relative weights"]

    # Optional plotting, which requires the "plot" extra
    if plot_weights or plot_rescaled:
        try:
            import plotly.express as px
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "Plotting requires Plotly, which is an optional dependency. "
                "Install it with: pip install 'johnson-rwa[plot]'"
            ) from exc

        if plot_weights:
            fig = px.bar(weights.T, y="relative weights", title="Relative Weights")
            fig.show()

        if plot_rescaled:
            fig = px.bar(weights.T, y="rescaled relative weights", title="Rescaled Relative Weights")
            fig.show()

    return weights.T
