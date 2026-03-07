
# Setup

Instalar dependencias del proyecto usando **uv**:

```bash
pip install uv
uv sync
```

# Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con la clave secreta:

```env
SECRET_KEY=tu_secret_key
```

Para generar una secret key segura:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

# Inicializar la base de datos

Aplicar todas las migraciones pendientes para crear o actualizar las tablas:

```bash
uv run alembic upgrade head
```

Esto aplicará todas las migraciones existentes dentro de `alembic/versions` y dejará la base de datos en el último estado del esquema.

# Crear una nueva migración (cuando cambian los modelos)

Cuando modifiques los modelos SQLAlchemy en `app/models/`, genera una nueva migración:

```bash
uv run alembic revision --autogenerate -m "describe el cambio"
```

Esto creará un nuevo archivo dentro de:

```
alembic/versions/
```

⚠️ Siempre revisa el archivo generado antes de aplicarlo.

# Aplicar la nueva migración

Después de generar la migración, aplícala a la base de datos:

```bash
uv run alembic upgrade head
```

# Problema común

Si Alembic muestra el error:

```
Target database is not up to date
```

Primero ejecuta:

```bash
uv run alembic upgrade head
```

y luego vuelve a generar la migración.

# Ejecutar la aplicación

```bash
uv run fastapi dev app/main.py
```
