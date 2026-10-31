# devops-10-2026

API de tarefas (FastAPI + SQLModel) e serviço de notificações, do módulo de extensão DevOps.

## Rodar os testes

```bash
pip install -r requirements.txt
pylint app tests
pytest --cov=app
```

Sem as variáveis `DATABASE_*` a API usa SQLite em memória, então os testes não precisam de banco.

## Rodar tudo com Docker

```bash
cp .env.example .env   # e troque as senhas
docker compose up --build
```

- Tarefas: http://localhost:8000/tarefas
- Notificações: `POST http://localhost:8000/notificar?_id=1&titulo=teste`

## Banco de dados

A API escolhe o banco nesta ordem:

1. `DATABASE_URL` (qualquer URL do SQLAlchemy);
2. MySQL com `DATABASE_USERNAME`, `DATABASE_PASSWORD`, `DATABASE_ADDRESS`, `DATABASE` (e `DATABASE_PORT`, padrão 3306);
3. SQLite em memória.
