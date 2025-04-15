from typing import Optional

import numpy as np
import pandas as pd
import plotly.express as px


def johnson_relative_weights(
    df: pd.DataFrame,
    x_vars: Optional[list] = None,
    y_var: Optional[str] = None,
    plot_weights: bool = False,
    plot_rescaled: bool = False,
) -> pd.DataFrame:
    """Calculates Johnson's Relative Weights for Regression results. This helps us determine the variables that contribute the most to R-squared

    Parameters
    ----------
    df : pandas DataFrame
        DataFrame containing our data
    x_vars : list, default=None
        A list containing all X variables for our regression. Optional if y is provided
    y_var : str
        A string of our y-variable metric. Optional if X is provided
    plot_weights : bool, default=False
        Whether to plot the weights
    plot_rescaled : bool, default=False
        Whether to plot the rescaled weights

    Returns
    -------
    weights : pandas DataFrame
        The Johnson's relative weights for each variable in X as well as the rescaled weights

    Notes
    -----
    https://www.statisticshowto.com/relative-weights/#:~:text=Johnson's%20Relative%20Weights%20is%20a,the%20most%20to%20r%2Dsquared.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if y_var is None:
        if x_vars is not None:
            y_var = df.columns.difference(x_vars)
        else:
            raise ValueError("y_var must be provided")
    if x_vars is None:
        if y_var is not None:
            x_vars = df.columns.difference(y_var)
        else:
            raise ValueError("x_var must be provided")
    new_df = df[sum([[y_var], x_vars], [])]
    correlation_matrix = new_df.corr()
    y_corr = correlation_matrix[y_var].drop(y_var, axis=0)
    x_corr = correlation_matrix[x_vars].drop(y_var, axis=0)
    eig_val, eig_vec = np.linalg.eig(x_corr)
    diag_eig = np.diagflat(eig_val)
    sqrt_diag_eig_val = np.sqrt(diag_eig)
    eigen_vec_t = eig_vec.T
    lamda = np.matmul(np.matmul(eig_vec, sqrt_diag_eig_val), eigen_vec_t)
    inv_lamda = np.linalg.inv(lamda)
    lamda_squared = np.square(lamda)
    partial_effect = np.matmul(inv_lamda, y_corr)
    r_squared = np.sum(np.square(partial_effect))
    raw_relative_weight = np.matmul(lamda_squared, np.square(partial_effect))
    weights = pd.DataFrame(
        np.array([raw_relative_weight, raw_relative_weight * 100 / r_squared]).reshape(
            2, len(x_vars)
        ),
        columns=x_vars,
    )
    weights.index = ["relative weights", "rescaled relative weights"]
    if plot_weights:
        fig = px.bar(weights.T, y="relative weights", title="Relative Weights")
        fig.show()
    if plot_rescaled:
        fig = px.bar(
            weights.T, y="rescaled relative weights", title="Rescaled Relative Weights"
        )
        fig.show()
    return weights.T
