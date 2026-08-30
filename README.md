# MED SYSTEM CRM

Информационная система для автоматизации деятельности медицинской компании. Проект объединяет управление складом, финансами, CRM, документами и табелем сотрудников в единой системе.

## Стек

- **FastAPI**
- **SQLAlchemy (async)**
- **PostgreSQL**
- **Alembic**
- **Poetry**
- **Docker**

## Статус

В разработке, учебный проект.

## Запуск
В файле .env перед запуском необходимо поменять SECRET_KEY
```
poetry install
poetry run uvicorn app.main:app --reload
cp .env.example .env
```