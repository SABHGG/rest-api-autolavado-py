import pytest


@pytest.fixture
def auth_token(client):
    # Registrar usuario
    client.post(
        "/auth/register",
        json={
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "123456789",
            "phone": "3027938664",
        },
    )
    # Login para obtener token
    response = client.post(
        "/auth/login",
        json={
            "email": "test2@example.com",
            "password": "123456789",
        },
    )
    return response.get_json()["access_token"]


def test_register_vehicle(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/vehicles/",
        json={
            "plate": "ABC223",
            "brand": "Ford",
            "model": "Raptor 2022",
            "color": "verde",
            "vehicle_type": "coche",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["brand"] == "Ford"
    assert data["model"] == "Raptor 2022"
    assert data["plate"] == "ABC223"


def test_register_vehicle_invalid_data(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/vehicles/",
        json={
            "plate": "ABC243",
            # "brand": "Ford", -- campo faltante
            "model": "Raptor 2022",
            "color": "verde",
            "vehicle_type": "coche",
        },
        headers=headers,
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "brand" in data


def test_get_user_vehicles(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Primero registrar algunos vehículos
    vehicles = [
        {
            "plate": "ABC423",
            "brand": "Toyota",
            "model": "Party",
            "color": "verde",
            "vehicle_type": "coche",
        },
        {
            "plate": "XYZ789",
            "brand": "Honda",
            "model": "civic",
            "color": "verde",
            "vehicle_type": "coche",
        },
    ]
    for vehicle in vehicles:
        client.post("/vehicles/", json=vehicle, headers=headers)

    # Obtener vehículos del usuario
    response = client.get("/vehicles/", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 3
    assert (
        data[0]["brand"] == "Ford"
    )  # Verifica el vehículo registrado en test_register_vehicle
    assert data[1]["brand"] == "Toyota"
    assert data[2]["brand"] == "Honda"


def test_register_vehicle_unauthorized(client):
    # Intentar registrar vehículo sin token
    response = client.post(
        "/vehicles/",
        json={
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2020,
            "color": "Rojo",
            "license_plate": "ABC123",
        },
    )
    assert response.status_code == 401
