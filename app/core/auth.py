from datetime import UTC, datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from app.core.config import settings

password_hasher = PasswordHash.recommended()

# Explicacion: El esquema de OAuth2PasswordBearer se utiliza para definir el punto de acceso donde los clientes
# pueden obtener un token de acceso. En este caso, el token se obtiene a través de la ruta "/api/users/token".
# Este esquema es parte del proceso de autenticación y autorización en aplicaciones web, permitiendo a los
# usuarios autenticarse y obtener un token que luego pueden usar para acceder a recursos protegidos.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hasher.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Crea un token de acceso JWT con los datos proporcionados y una fecha de expiración opcional."""
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def verify_access_token(token: str) -> dict | None:
    """Verifica un token de acceso JWT y devuelve los datos decodificados si el token es válido."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
        )
        return payload
    except jwt.PyJWTError:
        return None
