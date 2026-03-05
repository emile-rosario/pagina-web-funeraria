"""Tests de CRUD de ataúdes con permisos."""


class TestCoffinsPublic:
    def test_listar_ataudes_vacio(self, client):
        response = client.get("/ataudes")
        assert response.status_code == 200
        assert response.json() == []

    def test_listar_ataudes_con_datos(self, client, admin_token):
        # Crear uno como admin
        client.post("/ataudes", json={
            "nombre": "Ataúd Premium",
            "material": "Caoba",
            "precio": 25000.0,
        }, headers={"Authorization": f"Bearer {admin_token}"})

        # Listar sin token (público)
        response = client.get("/ataudes")
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestCoffinsAdmin:
    def test_crear_ataud(self, client, admin_token):
        response = client.post("/ataudes", json={
            "nombre": "Ataúd Clásico",
            "material": "Pino",
            "precio": 15000.0,
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Ataúd Clásico"
        assert data["id"] is not None

    def test_editar_ataud(self, client, admin_token):
        # Crear
        create_resp = client.post("/ataudes", json={
            "nombre": "Original",
            "material": "Pino",
            "precio": 10000.0,
        }, headers={"Authorization": f"Bearer {admin_token}"})
        coffin_id = create_resp.json()["id"]

        # Editar
        response = client.put(f"/ataudes/{coffin_id}", json={
            "nombre": "Editado",
            "precio": 12000.0,
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert response.json()["nombre"] == "Editado"
        assert response.json()["precio"] == 12000.0

    def test_eliminar_ataud(self, client, admin_token):
        create_resp = client.post("/ataudes", json={
            "nombre": "Para borrar",
            "material": "Pino",
            "precio": 5000.0,
        }, headers={"Authorization": f"Bearer {admin_token}"})
        coffin_id = create_resp.json()["id"]

        response = client.delete(
            f"/ataudes/{coffin_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204

        # Verificar que ya no existe
        response = client.get(f"/ataudes/{coffin_id}")
        assert response.status_code == 404


class TestCoffinsPermissions:
    def test_crear_sin_token_falla(self, client):
        response = client.post("/ataudes", json={
            "nombre": "Test",
            "material": "Pino",
            "precio": 1000.0,
        })
        assert response.status_code == 401

    def test_crear_como_cliente_falla(self, client, user_token):
        response = client.post("/ataudes", json={
            "nombre": "Test",
            "material": "Pino",
            "precio": 1000.0,
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403

    def test_eliminar_como_cliente_falla(self, client, user_token, admin_token):
        # Admin crea
        create_resp = client.post("/ataudes", json={
            "nombre": "Test",
            "material": "Pino",
            "precio": 1000.0,
        }, headers={"Authorization": f"Bearer {admin_token}"})
        coffin_id = create_resp.json()["id"]

        # Cliente intenta borrar
        response = client.delete(
            f"/ataudes/{coffin_id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403
