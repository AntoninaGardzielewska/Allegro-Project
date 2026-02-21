# Allegro-Project
[![CI](https://github.com/AntoninaGardzielewska/Allegro-Project/actions/workflows/ci.yml/badge.svg)](https://github.com/AntoninaGardzielewska/Allegro-Project/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-0%25-red)]()
[![Security](https://img.shields.io/badge/security-passed-brightgreen)]()

A Python application that allows users to create a shopping list and automatically finds the best price for each item on Allegro.

# Testing and Code Quality
We use a professional CI setup to ensure code quality. To run checks locally:
```bash
    # Run all tests with coverage
    pytest --cov=src --cov-report=xml

    # Linting & formatting
    uvx ruff check .
    uvx ruff format --check .

    # Type checking
    uvx mypy src/

    # Security checks
    bandit -r src/
    pip-audit
```
All tests and checks are run automatically on every commit via GitHub Actions.