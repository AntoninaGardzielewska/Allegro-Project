# Allegro-Project
[![CI](https://github.com/AntoninaGardzielewska/Allegro-Project/actions/workflows/ci.yaml/badge.svg)](https://github.com/AntoninaGardzielewska/Allegro-Project/actions/workflows/ci.yaml)

A smart shopping assistant for Allegro that helps users create a shopping list and automatically finds the best combined deals, minimizing product and shipping costs.

## Current Achievements
The project is in early API integration and initial optimization algorithm stages. Achievements so far:
- FastAPI endpoints:
  - GET /health – application status
  - GET /offers – fetch offers (mock)
  - GET /offers/{offer_id} – offer details
  - GET /best_price – example best price logic
- Unit tests in pytest for endpoints and business logic
- CI/CD via GitHub Actions:
    - Tests with coverage (coverage)
    - Linting (ruff) and typing (mypy)
    - Security analysis (bandit)
- Virtual environment managed via poetry
- Repository ready for further expansion (Docker, database, authentication)

## Technology Slack
- Backend: Python 3.12+, FastAPI
- Database: PostgreSQL (planned)
- Testing: pytest, coverage
- CI/CD: GitHub Actions
- Containerization: Docker + docker-compose (planned)
- Cloud / Deployment: AWS (planned)
- Other: OAuth2, JWT, SQLAlchemy, Pydantic, httpx

## Testing
- Unit tests for endpoints and business logic
- CI integration with coverage reporting
- Mocking of external APIs (planned in next phases)

## 🗺️ Future Development
The final version of the project will include:
- Full integration with Allegro API (OAuth2, token refresh, rate limit handling)
- Optimization algorithm for selecting the best combination of sellers for a shopping list
- Database models with SQLAlchemy and migrations
- Authentication and security (JWT, password hashing, role-based permissions)
- Dockerized environment for backend and database
- Cloud deployment with HTTPS, monitoring, and logs

## Running Locally
1. Clone the repository:
```
    git clone https://github.com/AntoninaGardzielewska/Allegro-Project.git
    cd Allegro-Project
```

2. Create and activate virtual environment:
```
    uv sync
```

3.Run tests:
```
    pytest --cov
```

4. Start FastAPI server:
```
    uvicorn src.allegro_project.main:app --reload
```

5. Open Swagger UI:
```
    http://127.0.0.1:8000/docs
```
