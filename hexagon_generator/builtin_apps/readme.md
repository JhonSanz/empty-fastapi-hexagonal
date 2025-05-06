- To excecute your project run `docker compose -f .\docker-compose.yml up --build`
- You will have some TODO in the code, please check them out and implement them.

---

1. In the same folder where alembic.ini is, run `alembic revision --autogenerate -m "Initial migration"` to generate the migrations file.
2. Run `alembic upgrade head` to apply the migrations to the database.
