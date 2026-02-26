# Contributing to rwa

Thank you for your interest in contributing to rwa! This document provides guidelines and instructions for contributing.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/ConorMcNamara/rwa.git
cd rwa
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev,test]"
```

## Development Workflow

### Code Style

This project uses:
- **ruff** for linting and formatting
- **mypy** for static type checking
- **pydocstringformatter** for docstring formatting

Before committing, run:
```bash
# Format code
ruff format src tests

# Check and fix linting issues
ruff check --fix src tests

# Type check
mypy src/rwa
```

### Testing

Run tests with pytest:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/rwa --cov-report=html

# Run specific test file
pytest tests/test_rwa.py -v
```

### Type Hints

All new code should include proper type hints. We enforce strict type checking with mypy.

Example:
```python
def my_function(x: int, y: str) -> bool:
    """Document your function."""
    return True
```

### Documentation

- All public functions and classes must have docstrings
- Use NumPy-style docstrings
- Include examples in docstrings when appropriate

Example:
```python
def example_function(param1: int, param2: str) -> bool:
    """Brief description of the function.

    Longer description if needed.

    Parameters
    ----------
    param1 : int
        Description of param1
    param2 : str
        Description of param2

    Returns
    -------
    bool
        Description of return value

    Examples
    --------
    >>> example_function(1, "hello")
    True
    """
    pass
```

## Pull Request Process

1. Fork the repository
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation as needed
7. Commit your changes with clear, descriptive messages
8. Push to your fork
9. Submit a pull request

### Commit Message Guidelines

Follow conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for test additions or modifications
- `chore:` for maintenance tasks

Example:
```
feat: add support for weighted regression analysis

- Implements weighted relative weights calculation
- Adds new parameter 'weights' to johnson_relative_weights
- Updates documentation with examples
```

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about the code
- Suggestions for improvements

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
