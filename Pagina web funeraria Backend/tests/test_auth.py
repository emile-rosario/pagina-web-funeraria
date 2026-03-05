"""Tests de autenticación: registro, login, y perfil."""


class TestRegister:
    def test_registro_exitoso(self, client):
        response = client.post("/register", json={
            "nombre": "Juan Pérez",
            "email": "juan@correo.com",
            "telefono": "8091234567",
            "password": "password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Juan Pérez"
        assert data["email"] == "juan@correo.com"
        assert data["rol"] == "cliente"
        assert "password" not in data

    def test_registro_email_duplicado(self, client):
        payload = {
            "nombre": "Juan Pérez",
            "email": "juan@correo.com",
            "telefono": "8091234567",
            "password": "password123",
        }
        client.post("/register", json=payload)
        response = client.post("/register", json=payload)
        assert response.status_code == 400
        assert "ya existe" in response.json()["detail"]

    def test_registro_password_muy_corta(self, client):
        response = client.post("/register", json={
            "nombre": "Juan",
            "email": "juan@correo.com",
            "telefono": "8091234567",
            "password": "123",  # Muy corta (min 8)
        })
        assert response.status_code == 422  # Error de validación


class TestLogin:
    def test_login_exitoso(self, client):
        # Registrar primero
        client.post("/register", json={
            "nombre": "Maria",
            "email": "maria@correo.com",
            "telefono": "8091111111",
            "password": "password123",
        })
        # Login
        response = client.post("/login", json={
            "email": "maria@correo.com",
            "password": "password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user_name"] == "Maria"

    def test_login_credenciales_incorrectas(self, client):
        response = client.post("/login", json={
            "email": "noexiste@correo.com",
            "password": "password123",
        })
        assert response.status_code == 401

    def test_login_password_incorrecta(self, client):
        client.post("/register", json={
            "nombre": "Pedro",
            "email": "pedro@correo.com",
            "telefono": "8092222222",
            "password": "password123",
        })
        response = client.post("/login", json={
            "email": "pedro@correo.com",
            "password": "wrongpassword",
        })
        assert response.status_code == 401


class TestProfile:
    def test_perfil_con_token(self, client, user_token):
        response = client.get("/me", headers={
            "Authorization": f"Bearer {user_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "cliente@test.com"
        assert data["rol"] == "cliente"

    def test_perfil_sin_token(self, client):
        response = client.get("/me")
        assert response.status_code == 401
