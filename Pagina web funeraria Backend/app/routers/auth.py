"""
Router de autenticación — registro, login y perfil del usuario.
"""
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, LoginRequest, UserResponse
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user_from_db,
    get_db,
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Autenticación"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario."""
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este correo ya existe.",
        )

    new_user = User(
        nombre=user_data.nombre,
        email=user_data.email,
        telefono=user_data.telefono,
        password=hash_password(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info("Usuario registrado: %s", new_user.email)
    return new_user


@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Iniciar sesión y obtener un token JWT."""
    db_user = db.query(User).filter(User.email == login_data.email).first()
    if not db_user or not verify_password(login_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas.",
        )

    token = create_access_token(data={"sub": db_user.email, "rol": db_user.rol})
    logger.info("Login exitoso: %s", db_user.email)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_name": db_user.nombre,
        "user_rol": db_user.rol,
    }


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user_from_db)):
    """Obtener el perfil del usuario autenticado."""
    return current_user
