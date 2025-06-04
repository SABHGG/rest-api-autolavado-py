def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "123456789",
            "phone": "3027338664",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Usuario registrado exitosamente"


def test_register_user_existing_username(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test1@example.com",
            "password": "123456789",
            "phone": "3027338664",
        },
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "El nombre de usuario ya existe"


def test_register_user_existing_email(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser2",
            "email": "test@example.com",
            "password": "123456789",
            "phone": "3027438664",
        },
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "El correo electrónico ya existe"


def test_register_user_existing_phone(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser3",
            "email": "test1cls@example.com",
            "password": "123456789",
            "phone": "3027338664",
        },
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "El número de teléfono ya existe"


def test_login_user(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "123456789",
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data


def test_login_user_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "Credenciales inválidas"
