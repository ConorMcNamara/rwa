.PHONY: help install install-dev lock test test-cov lint format type-check check clean build publish-test docs

# Default target
help:
	@echo "Available targets:"
	@echo "  install        - Install runtime dependencies only"
	@echo "  install-dev    - Sync the full dev environment (all groups and extras)"
	@echo "  lock           - Re-resolve and update uv.lock"
	@echo "  test           - Run tests"
	@echo "  test-cov       - Run tests with coverage report"
	@echo "  lint           - Run ruff linter"
	@echo "  format         - Auto-format code with ruff, autopep8, and pydocstringformatter"
	@echo "  type-check     - Run zuban type checker"
	@echo "  check          - Run all checks (lint, format check, type-check, test)"
	@echo "  clean          - Remove build artifacts and cache files"
	@echo "  build          - Build distribution packages"
	@echo "  publish-test   - Build and upload to TestPyPI"
	@echo "  docs           - Build documentation (if applicable)"

# Installation
install:
	uv sync --no-default-groups

install-dev:
	uv sync --all-extras

lock:
	uv lock

# Testing
test:
	uv run pytest tests/

test-cov:
	uv run pytest tests/ --cov=src/rwa --cov-report=html --cov-report=term

# Linting
lint:
	uv run ruff check src tests
	uv run ruff format --check src tests

# Formatting
format:
	uv run ruff format src tests
	uv run ruff check --fix src tests
	uv run autopep8 --in-place --recursive src tests
	uv run pydocstringformatter -w --style=numpydoc src tests

# Type checking
type-check:
	uv run zuban check src/rwa

# Run all checks
check: lint type-check test
	@echo "All checks passed!"

# Clean up
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf src/*.egg-info
	rm -rf .pytest_cache/
	rm -rf .zuban_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Build distribution
build: clean
	uv build
	uv run twine check --strict dist/*

# Dry-run release against TestPyPI
publish-test: build
	uv run twine upload --repository testpypi dist/*

# Documentation (placeholder - add if you use sphinx or mkdocs)
docs:
	@echo "Documentation target not yet configured"
