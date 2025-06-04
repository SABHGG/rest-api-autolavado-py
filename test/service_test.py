import pytest


@pytest.fixture
def admin_token(client):
    # Login con el administrador existente
    response = client.post(
        "/auth/login",
        json={
            "email": "sabh@gmail.com",
            "password": "123456789",
        },
    )
    return response.get_json()["access_token"]


def test_create_service(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/services/",
        json={
            "name": "Lavado Básico",
            "price": 50.00,
            "description": "Lavado exterior básico",
            "duration": 30,
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Lavado Básico"
    assert data["price"] == 50.00


def test_create_service_invalid_data(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/services/",
        json={
            "name": "Lavado Básico",
            # Falta el precio requerido
            "description": "Lavado exterior básico",
        },
        headers=headers,
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["price"] == ["Missing data for required field."]


def test_get_services(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Primero crear algunos servicios
    services = [
        {
            "name": "Lavado Básico",
            "price": 50.00,
            "description": "Lavado exterior básico",
            "duration": 30,
        },
        {
            "name": "Lavado Premium",
            "price": 100.00,
            "description": "Lavado completo",
            "duration": 60,
        },
    ]
    for service in services:
        client.post("/services/", json=service, headers=headers)

    # Obtener todos los servicios
    response = client.get("/services/", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 8
    assert data[0]["name"] == "Lavado Exterior Básico"
    assert data[-1]["name"] == "Lavado Premium"


def test_create_service_unauthorized(client):
    # Intentar crear servicio sin token de admin
    response = client.post(
        "/services/",
        json={
            "name": "Lavado Básico",
            "price": 50.00,
            "description": "Lavado exterior básico",
            "duration": 30,
        },
    )
    assert response.status_code == 401
