### First steps

- To excecute your project run `docker compose -f .\docker-compose.yml up --build`
- You will have some TODO in the code, please check them out and implement them.
- Register each builtin app's router in `src/common/router.py` and its exception
  mapping in `src/common/exceptions_mapping.py` — both are manual TODOs by design.

---

### Choosing an auth flavor: `auth` vs `cognito_auth`

Two mutually exclusive user/auth bundles are available — pick **one** per project,
never both:

- **`auth` + `user`**: local password auth (bcrypt + your own JWT, `SECRET_KEY`-signed).
- **`cognito_auth` + `cognito_user`**: AWS Cognito handles login/signup/password reset
  (frontend talks to Cognito directly); the backend only verifies the Cognito ID
  token against your User Pool's JWKS and JIT-provisions a local shadow `User` row
  on first sight of a given `cognito_sub`. Needs `COGNITO_USER_POOL_ID`,
  `COGNITO_REGION` and `COGNITO_APP_CLIENT_ID` set (see `src/config.py`).

Both flavors use the **same** `role` (Role/Permission RBAC) module unchanged, and
both expose an identically-shaped `get_user_with_permission(...)` dependency — but
`role` and `smtp` hardcode `from src.auth.dependencies...` by default. If you're
using `cognito_auth`, change that one import in `role/infrastructure/web.py` and
`smtp/infrastructure/web.py` to `from src.cognito_auth.dependencies...` (already
flagged with a `# NOTE:` comment right above that import in both files).

`user` and `cognito_user` intentionally share the same table names (`User`,
`UserRoleAssociation`) so `role`'s relationships resolve either way — which also
means **never generate both `user` and `cognito_user` into the same project**
(SQLAlchemy will raise `InvalidRequestError: Table 'User' is already defined...`
at import time if you do).

---

### Migrations

Inside the api container, you can run the following commands to manage your database migrations using Alembic:

1. `docker exec PS_ID  alembic revision --autogenerate -m "Initial migration"` to generate the migrations file.
2. `docker exec PS_ID  alembic upgrade head` to apply the migrations to the database.
