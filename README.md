# Sakila

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/Mandroide/cms-otek-backend/refs/heads/main/pyproject.toml)

This is an implementation of Sakila in FASTAPI.

The environment variables must be modified before running the app

Basic Structure of the project
```
.
├── pyproject.toml        # single source of truth (deps, tools, scripts)
├── README.md
├── .env                  # local defaults; never commit secrets
├── .pre-commit-config.yaml
├── .gitignore
├── Dockerfile            # reproducible image
├── scripts/              # one-shot helper scripts (DB seed, smoke-test…)
│   └── load_demo_data.py
├── alembic.ini           # if you use Alembic
├── alembic/              # migrations
├── tests/                # pytest & httpx tests (unit / integration / e2e)
│   ├── conftest.py
│   └── api/
│       └── test_films.py
└── src/                  # <— *src* layout prevents import shadowing
    └── app/              # import path is `app.*`
        ├── __init__.py
        ├── main.py       # ASGI entry-point → `uvicorn app.main:app`
        │
        ├── core/         # cross-cutting stuff
        │   ├── config.py         # Pydantic Settings / env parsing
        │   ├── logging.py
        │   └── security.py       # JWT utils, pwd hashing…
        │
        ├── db/                    # persistence layer
        │   ├── __init__.py        # exposes `async_session`
        │   ├── session.py         # engine & session factory
        │   ├── models/            # SQLModel or SQLAlchemy ORM tables
        │   │   └── film.py
        │   └── repositories/      # thin CRUD wrappers (optional)
        │       └── film.py
        │
        ├── api/                   # “outer” layer
        │   ├── __init__.py
        │   ├── deps.py            # FastAPI `Depends()` callables
        │   ├── v1/                # versioned APIs
        │   │   ├── __init__.py
        │   │   ├── routers/       # `APIRouter`s, 1 per resource
        │   │   │   └── films.py
        │   │   └── schemas/       # Pydantic models ↔ API IO
        │   │       ├── film.py
        │   │       └── common.py
        │   └── health.py          # /health, /metrics, …
        │
        ├── services/              # business logic (or “use-cases”)
        │   └── film_service.py
        │
        ├── tasks/                 # background jobs (Celery, RQ…)
        │   └── nightly_cleanup.py
        │
        └── utils/                 # small helpers, validators, etc.
            └── exceptions.py

```
## How to get started
```bash
poetry run pre-commit install --hook-type pre-commit --hook-type pre-push --hook-type commit-msg
```

## References
- [FastAPI](https://fastapi.tiangolo.com/)
- [Structuring FastAPI Projects: Best Practices for Clean and Scalable Code](https://medium.com/@agusabdulrahman/structuring-fastapi-projects-best-practices-for-clean-and-scalable-code-a993b297ea3a)
- [Microservices with FastAPI and poetry project management](https://tomasgis.com/microservices-with-fastapi-and-poetry-project-management-4c2c49f0fdda)
