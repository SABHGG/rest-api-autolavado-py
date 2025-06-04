import pytest


@pytest.fixture
def auth_token(client):
    # Registrar usuario
    client.post(
        "/auth/register",
        json={
            "username": "testuser1",
            "email": "test1@example.com",
            "password": "123456789",
            "phone": "3027638664",
        },
    )
    # Login para obtener token
    response = client.post(
        "/auth/login",
        json={
            "email": "test1@example.com",
            "password": "123456789",
        },
    )
    return response.get_json()["access_token"]


@pytest.fixture
def auth_token_employee(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "sabh-employee@gmail.com",
            "password": "123456789",
        },
    )
    return response.get_json()["access_token"]


def test_create_appointment(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/appointments",
        json={
            "appointment_time": "2025-06-05T10:00:00",
            "vehicle_id": "ABC123",
            "status": "pendiente",
            "services": [{"service_id": 1}],
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert response.get_json()["id"]


def test_get_appointments(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(
        "/appointments", headers=headers
    )  # Imprimir la respuesta para depuración
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_appointment(client, auth_token):
    # Primero crear una cita
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Obtener la cita específica
    response = client.get("/appointments/91", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 91


def test_assign_appointment(client, auth_token_employee):
    headers = {"Authorization": f"Bearer {auth_token_employee}"}
    # Asignar empleado
    response = client.patch("/appointments/91/assign", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Services assigned successfully"


def test_update_appointment_status(client, auth_token_employee):
    # Primero crear una cita
    headers = {"Authorization": f"Bearer {auth_token_employee}"}

    # Actualizar estado
    response = client.patch(
        "/appointments/91/status", json={"status": "en_progreso"}, headers=headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "en_progreso"


def test_update_appointment_invalid_status(client, auth_token_employee):
    headers = {"Authorization": f"Bearer {auth_token_employee}"}
    response = client.patch(
        "/appointments/91/status", json={"status": "estado_invalido"}, headers=headers
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "message" in data
