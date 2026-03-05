from pydantic import BaseModel, EmailStr, Field


# --- Schemas de Registro ---

class UserCreate(BaseModel):
    """Lo que recibimos del Frontend al registrarse."""
    nombre: str = Field(min_length=2, max_length=100)
    email: EmailStr
    telefono: str = Field(min_length=7, max_length=20)
    password: str = Field(min_length=8, max_length=100)


# --- Schema de Login ---

class LoginRequest(BaseModel):
    """Solo email y contraseña para iniciar sesión."""
    email: EmailStr
    password: str


# --- Schema de Respuesta ---

class UserResponse(BaseModel):
    """Lo que enviamos de vuelta al cliente (sin el password)."""
    id: int
    nombre: str
    email: EmailStr
    telefono: str
    rol: str

    model_config = {"from_attributes": True}