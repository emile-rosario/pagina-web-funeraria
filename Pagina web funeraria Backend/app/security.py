"""
Módulo de seguridad — Funeraria Rancier
Maneja hashing de contraseñas, generación/validación de JWT,
y dependencias de autenticación para FastAPI.
"""
import logging
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings

logger = logging.getLogger(__name__)

# Esquema OAuth2 — extrae el token del header "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# --- FUNCIONES DE CONTRASEÑA (BCRYPT) ---

def hash_password(password: str) -> str:
    """Convierte la contraseña plana en un hash seguro."""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña escrita coincide con la guardada."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# --- FUNCIONES DE TOKEN (JWT) ---

def create_access_token(data: dict) -> str:
    """Genera un token JWT firmado con tiempo de expiración."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    logger.info("Token JWT generado para: %s", data.get("sub"))
    return encoded_jwt


# --- DEPENDENCIAS DE AUTENTICACIÓN ---

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependencia de FastAPI que valida el token JWT.
    Retorna el email del usuario autenticado.
    Uso: current_user = Depends(get_current_user)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el acceso.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        logger.warning("Intento de acceso con token inválido")
        raise credentials_exception


def get_db():
    """Dependencia que proporciona una sesión de base de datos."""
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_from_db(
    email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Dependencia que retorna el objeto User completo de la base de datos.
    Uso: user = Depends(get_current_user_from_db)
    """
    from app.models.user import User

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado.",
        )
    return user


def get_current_admin(
    current_user=Depends(get_current_user_from_db),
):
    """
    Dependencia que verifica que el usuario autenticado sea administrador.
    Uso: admin = Depends(get_current_admin)
    """
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador.",
        )
    return current_user