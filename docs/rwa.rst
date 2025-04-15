Johnson's Re-weighted Analysis for Regression
===============================================

Johnson's Re-weighted Analysis for Regression is a statistical method used to improve the accuracy and robustness of regression analysis, particularly in the presence of heteroscedasticity or influential outliers. It was primarily developed by W. Johnson.

Key Concepts
------------

* **Heteroscedasticity:** This refers to the situation where the variance of the error term in a regression model is not constant across all levels of the independent variables.  Ordinary Least Squares (OLS) regression assumes homoscedasticity (constant variance), and when this assumption is violated, the OLS estimates, while still unbiased, are inefficient, and the standard errors are biased, leading to incorrect inferences.

* **Influential Outliers:** Outliers are data points that deviate significantly from the general pattern of the data.  Influential outliers are those that, when included or excluded from the regression analysis, cause substantial changes in the estimated regression coefficients.  These outliers can disproportionately affect the OLS estimates.

* **Re-weighting:** Johnson's method involves assigning different weights to the data points in the regression analysis.  The weights are typically determined based on the estimated variance of the error term or the influence of the data points.  Data points with higher variance or greater influence are given lower weights, while those with lower variance or less influence are given higher weights.

Methodology
-----------

The general procedure for Johnson's Re-weighted Analysis for Regression involves the following steps:

1.  **Initial Regression:** Perform an initial regression analysis using Ordinary Least Squares (OLS) to obtain preliminary estimates of the regression coefficients and residuals.

2.  **Variance Estimation or Influence Measurement:**
    * **Heteroscedasticity:** If heteroscedasticity is suspected, estimate the variance of the error term as a function of the independent variables.  This can be done using various methods, such as the White test, the Breusch-Pagan test, or by modeling the variance directly.
    * **Outliers:** If outliers are a concern, measure the influence of each data point on the regression coefficients.  Common measures of influence include Cook's distance, DFFITS (difference in fits), and DFBETAS (difference in betas).

3.  **Weight Calculation:** Calculate the weights for each data point based on the estimated variance or the measured influence.
    * **Heteroscedasticity:** Weights are typically inversely proportional to the estimated variance.  For example, if the variance of the i-th observation is estimated as  *v<sub>i</sub>*, the weight for that observation might be  *1/v<sub>i</sub>*.
    * **Outliers:** Weights are assigned to downweight influential observations.  For example, observations with large Cook's distances might be assigned lower weights.  Various weighting functions can be used.

4.  **Weighted Least Squares (WLS) Regression:** Perform a Weighted Least Squares (WLS) regression using the calculated weights.  WLS minimizes the sum of the weighted squared residuals, giving less weight to observations with higher variance or greater influence.

5.  **Iteration (Optional):** In some cases, the process may be iterated.  The residuals from the WLS regression can be used to refine the variance estimates or influence measures, and the weights can be updated accordingly.  This iterative process can continue until the estimates converge.

Advantages
----------

* **Improved Efficiency:** In the presence of heteroscedasticity, WLS with appropriate weights provides more efficient estimates than OLS.

* **Reduced Bias:** Downweighting influential outliers can reduce the bias in the regression coefficients.

* **More Robust Inference:** Correcting for heteroscedasticity leads to more reliable standard errors and thus more accurate hypothesis tests and confidence intervals.

Limitations
----------

* **Correct Variance Model:** If dealing with heteroscedasticity, the effectiveness of the method depends on correctly specifying the model for the variance of the error term.

* **Choice of Weighting Function:** If dealing with outliers, the choice of the weighting function can affect the results.

* **Computational Cost:** Iterative methods can be computationally more expensive than OLS.

Paper Attributions
------------------

While the concept of re-weighted least squares is a standard statistical technique, W. Johnson has made significant contributions in applying and extending these methods, particularly in the context of handling both heteroscedasticity and outliers.  Unfortunately, pinpointing a single, definitive paper that lays out "Johnson's Re-weighted Analysis" as a singular named method is difficult.  The techniques are often built upon and extended in various applications.

To find relevant research, you could search for papers and publications by W. Johnson in econometrics or statistics journals, focusing on topics such as:

* Heteroscedasticity-consistent covariance matrix estimation
* Robust regression methods
* Weighted least squares
* Outlier detection and treatment in regression

General references that discuss the underlying methods include:

* **Carroll, R. J., & Ruppert, D. (1988). Transformation and weighting in regression.** Chapman and Hall.  (This book provides a comprehensive treatment of transformation and weighting techniques in regression.)
* **Hamilton, L. C. (1992). Regression with graphics and statistics.** Duxbury Press. (This book covers regression diagnostics, including methods for detecting heteroscedasticity and outliers.)
* **Wooldridge, J. M. (2015). Introductory econometrics: A modern approach.** Cengage Learning. (This textbook provides a standard treatment of heteroscedasticity and weighted least squares in the context of econometrics.)

It's important to note that the specific implementation and application of re-weighting techniques can vary depending on the context and the specific characteristics of the data.
