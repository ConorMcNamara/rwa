Johnson's Relative Weights Analysis
===================================

Relative Weights Analysis (RWA), also known as Key Drivers Analysis, decomposes
the variance explained by a linear regression model (:math:`R^2`) into
contributions attributable to each predictor. It was introduced by Jeff W.
Johnson in 2000 as a computationally tractable alternative to methods that
require evaluating every possible subset of predictors.

The Problem It Solves
---------------------

When predictors are correlated, the usual ways of judging "which variable matters
most" break down:

* **Standardized regression coefficients** are unstable under multicollinearity.
  A predictor's coefficient depends on which other predictors are in the model,
  so coefficients can shrink, grow, or flip sign as the model changes.

* **Squared zero-order correlations** ignore the other predictors entirely, so
  they double-count variance shared between correlated predictors and do not sum
  to :math:`R^2`.

RWA sidesteps both problems. It produces one non-negative weight per predictor,
and those weights sum exactly to the model's :math:`R^2`, so each can be read as
that predictor's share of explained variance.

Key Concepts
------------

* **Orthogonal transformation:** The core idea is to replace the correlated
  predictors :math:`X` with a set of uncorrelated variables :math:`Z` that are as
  close as possible to the original :math:`X`. Because the :math:`Z` variables
  are orthogonal, regressing the criterion on them yields coefficients that can
  be cleanly attributed, with no shared-variance ambiguity.

* **Relative weight:** Each predictor's contribution is recovered by combining
  (a) how strongly the orthogonal variables predict the criterion with (b) how
  strongly each original predictor maps onto each orthogonal variable.

* **Rescaled relative weight:** The raw weights expressed as a percentage of
  :math:`R^2`. These sum to 100 and are usually what gets reported, since they
  answer "what share of the model's predictive power does this driver own?"

Methodology
-----------

Let :math:`R_{xx}` be the correlation matrix among the :math:`p` predictors and
:math:`r_{xy}` the vector of correlations between each predictor and the
criterion.

1. **Eigendecomposition of the predictor correlation matrix:**

   .. math::

      R_{xx} = V \Delta V'

   where :math:`V` holds the eigenvectors and :math:`\Delta` the eigenvalues on
   its diagonal. Because :math:`R_{xx}` is real and symmetric, this is computed
   with a symmetric eigensolver (``numpy.linalg.eigh``), which guarantees real
   eigenvalues and orthonormal eigenvectors.

2. **Construct the orthogonal approximation.** Form the symmetric square root of
   :math:`R_{xx}`:

   .. math::

      \Lambda = V \Delta^{1/2} V'

   :math:`\Lambda` is the matrix of correlations between the original predictors
   and their orthogonal counterparts :math:`Z = X \Lambda^{-1}`. Johnson showed
   that this choice makes :math:`Z` the set of orthogonal variables maximally
   related to the original predictors in a least-squares sense.

3. **Regress the criterion on the orthogonal variables:**

   .. math::

      \beta = \Lambda^{-1} r_{xy}

   Since the :math:`Z` variables are uncorrelated, these standardized
   coefficients are simply the correlations between :math:`Z` and the criterion.

4. **Recover the model fit.** Because the coefficients are orthogonal, their
   squares sum to the variance explained:

   .. math::

      R^2 = \sum_{k=1}^{p} \beta_k^2

5. **Combine the two pieces to get raw relative weights:**

   .. math::

      \varepsilon = \Lambda^{2} \beta^{2}

   where :math:`\Lambda^{2}` squares :math:`\Lambda` elementwise. Each
   :math:`\varepsilon_j` is non-negative, and the weights sum to :math:`R^2`.

6. **Rescale to percentages:**

   .. math::

      \varepsilon^{\text{rescaled}}_j = 100 \times \frac{\varepsilon_j}{R^2}

Interpretation
--------------

A rescaled weight of 30 means that predictor accounts for roughly 30% of the
variance the model explains — not 30% of the variance in the criterion overall.
Because the raw weights sum to :math:`R^2`, a model with a low :math:`R^2` can
still yield large rescaled weights; the rescaled values describe how explained
variance is distributed, not how much of it there is.

Relative weights are non-negative by construction, so they convey **magnitude
but not direction**. A predictor strongly *negatively* related to the criterion
receives a large weight. Inspect the sign of the zero-order correlations or the
regression coefficients alongside the weights to recover direction.

Assumptions and Limitations
---------------------------

* **Linear model.** RWA decomposes the :math:`R^2` of a linear regression. It
  says nothing about nonlinear or interactive effects unless those terms are
  entered as predictors explicitly.

* **Perfect collinearity is not permitted.** If a predictor is an exact linear
  combination of the others, :math:`R_{xx}` is singular, :math:`\Lambda` cannot
  be inverted, and the decomposition is undefined. This implementation raises a
  ``ValueError`` in that case. Ordinary multicollinearity — the situation RWA
  exists to handle — is fine; it is exact redundancy that fails.

* **Near-singular inputs are numerically fragile.** With predictors that are
  almost perfectly redundant, :math:`\Lambda^{-1}` is poorly conditioned and the
  raw weights can become very large, even while the rescaled weights remain
  interpretable.

* **No inferential output.** The implementation returns point estimates only. It
  does not provide standard errors, confidence intervals, or significance tests;
  bootstrapping is the usual approach when those are needed.

Relationship to Other Methods
-----------------------------

RWA typically produces results very close to **Shapley value regression** (also
called LMG or dominance analysis), which averages each predictor's incremental
:math:`R^2` across all possible predictor orderings. Shapley regression is
generally regarded as the more principled decomposition, but its cost grows
exponentially in the number of predictors, whereas RWA requires a single
eigendecomposition. For most applied problems the two agree closely, which is why
RWA is the practical default when predictor counts are large.

Usage
-----

.. code-block:: python

   import pandas as pd
   from rwa import johnson_relative_weights

   df = pd.DataFrame({
       "feature1": [1, 2, 3, 4, 5, 6, 7, 8],
       "feature2": [2, 1, 6, 3, 10, 5, 9, 7],
       "target":   [1, 3, 5, 4, 9, 7, 11, 10],
   })

   weights = johnson_relative_weights(df, x_vars=["feature1", "feature2"], y_var="target")
   print(weights)

.. code-block:: text

             relative weights  rescaled relative weights
   feature1          0.522441                  53.856458
   feature2          0.447621                  46.143542

The returned ``DataFrame`` is indexed by predictor name and has two columns:
``relative weights`` (summing to :math:`R^2`) and ``rescaled relative weights``
(summing to 100).

If ``x_vars`` is omitted it is inferred as every column except ``y_var``; if
``y_var`` is omitted it is inferred as the single column not listed in
``x_vars``. Passing ``plot_weights=True`` or ``plot_rescaled=True`` displays a
Plotly bar chart, which requires the optional ``plot`` extra
(``pip install "johnson-rwa[plot]"``).

References
----------

* Johnson, J. W. (2000). `A Heuristic Method for Estimating the Relative Weight
  of Predictor Variables in Multiple Regression
  <https://www.tandfonline.com/doi/abs/10.1207/S15327906MBR3501_1>`_.
  *Multivariate Behavioral Research*, 35(1), 1-19.

* Tonidandel, S., & LeBreton, J. M. (2015). `RWA Web: A Free, Comprehensive,
  Web-Based, and User-Friendly Tool for Relative Weight Analyses
  <https://link.springer.com/article/10.1007/s10869-014-9351-z>`_.
  *Journal of Business and Psychology*, 30(2), 207-216.

* Chan, M. (2020). `rwa: Perform a Relative Weights Analysis
  <https://cran.r-project.org/web/packages/rwa/rwa.pdf>`_. R package.
