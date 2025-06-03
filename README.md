# Sakila

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/Mandroide/cms-otek-backend/refs/heads/main/pyproject.toml)

This is an implementation of Sakila in FASTAPI.

The environment variables must be modified before running the app

Basic Structure of the project
```
my_project/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── controllers/
│   │       ├── __init__.py
│   │       └── items.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── item.py
│   ├── crud/
│   │   ├── __init__.py
│   │   └── item.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py
│   └── tests/
│       ├── __init__.py
│       └── test_items.py
├── .env
├── .env.example
├── .gitignore
├── poetry.lock
├── pyproject.toml
└── README.md
```
Reference: [Structuring FastAPI Projects: Best Practices for Clean and Scalable Code](https://medium.com/@agusabdulrahman/structuring-fastapi-projects-best-practices-for-clean-and-scalable-code-a993b297ea3a)
