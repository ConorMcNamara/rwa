# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Distribution renamed to `johnson-rwa`** for the first PyPI release; the name
  `rwa` on PyPI is taken by an unrelated project. The import name is unchanged
  (`import rwa`), so no code changes are required.
- **Plotly is now an optional dependency.** Install `johnson-rwa[plot]` to use
  `plot_weights` / `plot_rescaled`; requesting a plot without Plotly installed
  now raises `ImportError` with install instructions.
- Dependency management moved from Poetry to [uv](https://docs.astral.sh/uv/).
  `poetry.lock` (which was never actually in use) is replaced by a committed
  `uv.lock`; the Makefile and CI workflows now use `uv sync` / `uv run`.
- Dev and test dependencies moved from extras to PEP 735 `[dependency-groups]`,
  so they are no longer published as installable extras on PyPI. Use
  `uv sync --all-extras` instead of `pip install -e ".[dev,test]"`.
- Package version is now sourced solely from `rwa.__version__` via setuptools
  dynamic metadata, removing the duplicate version in `pyproject.toml`.
- License metadata migrated to the PEP 639 SPDX form (`license = "MIT"`).

### Added
- `Publish` GitHub Actions workflow that builds, verifies, and uploads to PyPI
  on `v*` tags using Trusted Publishing (OIDC, no stored API token). Includes a
  tag-vs-version consistency check and `twine check --strict`.
- `make publish-test` target for TestPyPI dry runs.
- Tests covering real-valued (non-complex) output and the perfect-collinearity
  error path.

### Fixed
- **Weights are now real-valued.** The eigendecomposition uses `np.linalg.eigh`
  instead of `np.linalg.eig`. The predictor correlation matrix is symmetric, so
  `eig` was returning a complex dtype whose zero-valued imaginary parts leaked
  into the returned DataFrame (weights printed as `0.469034+0.000000j`).
  Numerical results are unchanged, as verified against the reference R `rwa`
  package. Negative eigenvalues arising from floating-point noise are clipped to
  zero, since a correlation matrix is positive semi-definite.
- Perfectly collinear predictors now raise `ValueError` with an actionable
  message instead of a bare `numpy.linalg.LinAlgError: Singular matrix`.
- The README quick-start example no longer errors. Its predictors were perfectly
  collinear (`feature2 == 2 * feature1`), so the first example a user copied
  raised `LinAlgError`. It now uses non-collinear data and shows real output.
- **`docs/rwa.rst` rewritten.** It described "Johnson's Re-weighted Analysis," a
  method for heteroscedasticity and influential outliers using weighted least
  squares — not Relative Weights Analysis, and attributed to the wrong author.
  It now documents the algorithm actually implemented, with each equation
  verified against the code.
- The README no longer claims ">90% coverage"; actual coverage is ~80%.
- The sdist now includes `tests/conftest.py`, `tests/__init__.py`, and `docs/`,
  so the test suite is runnable from the source distribution.
- CONTRIBUTING.md no longer refers to mypy, which was replaced by zuban.

## [1.0.0] - 2026-02-26

### Added
- Initial release of rwa package
- Johnson's Relative Weights Analysis implementation
- Support for Python 3.13+
- Full type hints and mypy support
- Comprehensive test suite
- Optional Plotly visualizations
- Modern packaging with pyproject.toml
- GitHub Actions CI/CD workflows
- Comprehensive documentation

### Changed
- Migrated to src-layout package structure
- Modernized build system using setuptools
- Enhanced error handling and input validation

### Documentation
- Added comprehensive README with examples
- Added CONTRIBUTING guidelines
- Added LICENSE (MIT)
- Added type stubs (py.typed marker)

## Planned
- Add support for weighted regression
- Add more visualization options
- Performance optimizations for large datasets
