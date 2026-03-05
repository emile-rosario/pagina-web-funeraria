"""
Configuración compartida para todos los tests.
Usa una base de datos SQLite en memoria para no afectar la real.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app
from app.security import get_db, hash_password


# Base de datos de prueba (en memoria)
TEST_DATABASE_URL = "sqlite:///./test_funeraria.db"
engine_test = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Reemplazar la dependencia de DB en la app
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Crea las tablas antes de cada test y las elimina después."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def client():
    """Cliente HTTP de prueba."""
    return TestClient(app)


@pytest.fixture
def admin_token(client):
    """Crea un usuario admin y retorna su token."""
    # Crear admin directamente en la DB
    db = TestingSessionLocal()
    from app.models.user import User
    admin = User(
        nombre="Admin Test",
        email="admin@test.com",
        telefono="8091234567",
        password=hash_password("admin12345"),
        rol="admin",
    )
    db.add(admin)
    db.commit()
    db.close()

    # Login para obtener token
    response = client.post("/login", json={
        "email": "admin@test.com",
        "password": "admin12345",
    })
    return response.json()["access_token"]


@pytest.fixture
def user_token(client):
    """Crea un usuario normal y retorna su token."""
    client.post("/register", json={
        "nombre": "Cliente Test",
        "email": "cliente@test.com",
        "telefono": "8099876543",
        "password": "cliente12345",
    })
    response = client.post("/login", json={
        "email": "cliente@test.com",
        "password": "cliente12345",
    })
    return response.json()["access_token"]
