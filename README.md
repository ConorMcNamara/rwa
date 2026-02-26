# rwa - Johnson's Relative Weights Analysis

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Typed with mypy](https://img.shields.io/badge/typed-mypy-blue.svg)](http://mypy-lang.org/)

A modern Python implementation of Johnson's Relative Weights Analysis for regression models. This package helps estimate the contribution of each feature to the R-squared of a regression model.

## Overview

Relative Weights Analysis (RWA), also known as Key Drivers Analysis, decomposes the total variance predicted in a regression model into weights that accurately reflect the proportional contribution of predictor variables. This addresses the issue of multicollinearity that often plagues traditional regression interpretation methods.

In typical scenarios, RWA returns similar results to Shapley regression, but with significant computational performance advantages.

## Features

- ✨ Modern Python 3.13+ implementation with full type hints
- 📊 Calculate Johnson's relative weights for regression models
- 🎨 Optional interactive visualizations using Plotly
- 🧪 Comprehensive test suite with >90% coverage
- 📦 Clean, well-documented API
- 🔧 Fully typed and supports static type checking

## Installation

```bash
pip install rwa
```

For development:

```bash
git clone https://github.com/ConorMcNamara/rwa.git
cd rwa
pip install -e ".[dev]"
```

## Quick Start

```python
import pandas as pd
from rwa import johnson_relative_weights

# Load your data
df = pd.DataFrame({
    'feature1': [1, 2, 3, 4, 5],
    'feature2': [2, 4, 6, 8, 10],
    'target': [1, 3, 5, 7, 9]
})

# Calculate relative weights
weights = johnson_relative_weights(
    df,
    x_vars=['feature1', 'feature2'],
    y_var='target',
    plot_weights=True  # Optional: display visualization
)

print(weights)
```

## Usage

The main function `johnson_relative_weights()` accepts the following parameters:

- `df` (pd.DataFrame): DataFrame containing your data
- `x_vars` (list[str], optional): List of predictor variable names
- `y_var` (str, optional): Target variable name
- `plot_weights` (bool, default=False): Whether to display relative weights plot
- `plot_rescaled` (bool, default=False): Whether to display rescaled weights plot

The function returns a DataFrame with two columns:
- `relative weights`: Raw relative weights for each predictor
- `rescaled relative weights`: Weights scaled to sum to 100%

## Development

### Running Tests

```bash
pytest
```

### Type Checking

```bash
mypy src/rwa
```

### Linting and Formatting

```bash
ruff check .
ruff format .
```

## References

- **Tonidandel & LeBreton (2015)**: [RWA Web: A Free, Comprehensive, Web-Based, and User-Friendly Tool for Relative Weight Analyses](https://link.springer.com/article/10.1007/s10869-014-9351-z)
- **Martin Chan (2020)**: [Perform a Relative Weights Analysis (R package)](https://cran.r-project.org/web/packages/rwa/rwa.pdf)
- **Jeff Johnson (2000)**: [A Heuristic Method for Estimating the Relative Weight of Predictor Variables in Multiple Regression](https://www.tandfonline.com/doi/abs/10.1207/S15327906MBR3501_1)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{rwa2026,
  author = {McNamara, Conor},
  title = {rwa: Johnson's Relative Weights Analysis for Python},
  year = {2026},
  url = {https://github.com/ConorMcNamara/rwa}
}
```
