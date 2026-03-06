# Setup

```bash
pip install uv
uv sync
```

# Inicializar la base de datos

Ejecutar las migraciones para crear las tablas:

```bash
uv run alembic upgrade head
```

Esto aplicará todas las migraciones en `alembic/versions` y creará las tablas necesarias en la base de datos.

# Ejecutar la aplicación

```bash
uv run fastapi dev app/main.py
```
