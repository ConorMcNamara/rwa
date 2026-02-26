.PHONY: help install install-dev test test-cov lint format type-check check clean build docs

# Default target
help:
	@echo "Available targets:"
	@echo "  install        - Install package dependencies"
	@echo "  install-dev    - Install package with development dependencies"
	@echo "  test           - Run tests"
	@echo "  test-cov       - Run tests with coverage report"
	@echo "  lint           - Run ruff linter"
	@echo "  format         - Auto-format code with ruff, autopep8, and pydocstringformatter"
	@echo "  type-check     - Run mypy type checker"
	@echo "  check          - Run all checks (lint, format check, type-check, test)"
	@echo "  clean          - Remove build artifacts and cache files"
	@echo "  build          - Build distribution packages"
	@echo "  docs           - Build documentation (if applicable)"

# Installation
install:
	python -m pip install --upgrade pip
	pip install -e .

install-dev:
	python -m pip install --upgrade pip
	pip install -e ".[dev,test]"

# Testing
test:
	pytest tests/

test-cov:
	pytest tests/ --cov=src/rwa --cov-report=html --cov-report=term

# Linting
lint:
	ruff check src tests

# Formatting
format:
	ruff format src tests
	ruff check --fix src tests
	autopep8 --in-place --recursive src tests
	pydocstringformatter -w --style=numpydoc src tests

# Type checking
type-check:
	mypy src/rwa

# Run all checks
check: lint type-check test
	@echo "All checks passed!"

# Clean up
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Build distribution
build: clean
	python -m pip install --upgrade build
	python -m build

# Documentation (placeholder - add if you use sphinx or mkdocs)
docs:
	@echo "Documentation target not yet configured"
