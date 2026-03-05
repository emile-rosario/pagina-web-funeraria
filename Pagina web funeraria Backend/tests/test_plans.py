"""Tests de CRUD de planes funerarios con permisos."""


class TestPlansPublic:
    def test_listar_planes_vacio(self, client):
        response = client.get("/planes")
        assert response.status_code == 200
        assert response.json() == []


class TestPlansAdmin:
    def test_crear_plan(self, client, admin_token):
        response = client.post("/planes", json={
            "nombre": "Plan Básico",
            "descripcion": "Servicios básicos de sepelio",
            "precio_mensual": 500.0,
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Plan Básico"

    def test_editar_plan(self, client, admin_token):
        create_resp = client.post("/planes", json={
            "nombre": "Original",
            "descripcion": "Descripción original",
            "precio_mensual": 300.0,
        }, headers={"Authorization": f"Bearer {admin_token}"})
        plan_id = create_resp.json()["id"]

        response = client.put(f"/planes/{plan_id}", json={
            "nombre": "Editado",
            "precio_mensual": 450.0,
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert response.json()["nombre"] == "Editado"

    def test_eliminar_plan(self, client, admin_token):
        create_resp = client.post("/planes", json={
            "nombre": "Para borrar",
            "descripcion": "Se eliminará",
            "precio_mensual": 100.0,
        }, headers={"Authorization": f"Bearer {admin_token}"})
        plan_id = create_resp.json()["id"]

        response = client.delete(
            f"/planes/{plan_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204


class TestPlansPermissions:
    def test_crear_como_cliente_falla(self, client, user_token):
        response = client.post("/planes", json={
            "nombre": "Test",
            "descripcion": "Test plan",
            "precio_mensual": 100.0,
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403
