# Allegro-Project
[![CI](https://github.com/AntoninaGardzielewska/Allegro-Project/actions/workflows/ci.yaml/badge.svg)](https://github.com/AntoninaGardzielewska/Allegro-Project/actions/workflows/ci.yaml)

A Python application that allows users to create a shopping list and automatically finds the best price for each item on Allegro.

# Testing and Code Quality
Uses a professional CI setup to ensure code quality. To run checks locally:
```bash
    # Run all tests with coverage
    pytest --cov=src --cov-report=xml --cov-report=term-missing

    # Linting & formatting
    uvx ruff check .  # Check and optionally auto-fix issues
    uvx ruff format --check .

    # Type checking
    uvx mypy src/

    # Security checks
    bandit -r src/
    # Optional: run locally for dependency vulnerabilities (not executed in CI)
    pip-audit
```
All tests and checks are run automatically on every commit via GitHub Actions.