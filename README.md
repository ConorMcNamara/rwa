# rwa
Performs Johnson's Re-Weighed Analysis for Regression

A Python implementation of Johnson's Re-Weighted Analysis for Regression. Used to estimate the contribution of each feature to the R-squared of the model. To borrow from the r package [rwa](https://cran.r-project.org/web/packages/rwa/index.html), "Perform a Relative Weights Analysis (RWA) (a.k.a. Key Drivers Analysis)... In essence, RWA decomposes the total variance predicted in a regression model into weights that accurately reflect the proportional contribution of the predictor variables, which addresses the issue of multi-collinearity. In typical scenarios, RWA returns similar results to Shapley regression, but with a significant advantage on computational performance."

## References

* Tonidandel & LeBreton (2015) RWA Web: A Free, Comprehensive, Web-Based, and User-Friendly Tool for Relative Weight Analyses. https://link.springer.com/article/10.1007/s10869-014-9351-z
* Martin Chan (2020). Perform a Relative Weights Analysis. https://cran.r-project.org/web/packages/rwa/rwa.pdf
* Jeff Johnson (2000). A Heuristic Method for Estimating the Relative Weight of Predictor Variables in Multiple Regression. https://www.tandfonline.com/doi/abs/10.1207/S15327906MBR3501_1
