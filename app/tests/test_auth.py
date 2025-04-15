import pytest
from app.models.user import User, RoleEnum

def test_register_success(client):
    """Prueba el registro exitoso de un usuario."""
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'phone': '1234567890'
    })
    
    assert response.status_code == 201
    assert 'message' in response.json
    assert response.json['message'] == 'Usuario registrado exitosamente'
    
    # Verificar que el usuario se creó en la base de datos
    with client.application.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@example.com'
        assert user.role == RoleEnum.client.value

def test_register_duplicate_username(client):
    """Prueba el registro con un nombre de usuario que ya existe."""
    # Primero registrar un usuario
    client.post('/auth/register', json={
        'username': 'existinguser',
        'email': 'existing@example.com',
        'password': 'password123',
        'phone': '1234567890'
    })
    
    # Intentar registrar otro usuario con el mismo nombre de usuario
    response = client.post('/auth/register', json={
        'username': 'existinguser',
        'email': 'another@example.com',
        'password': 'password123',
        'phone': '0987654321'
    })
    
    assert response.status_code == 400
    assert 'message' in response.json
    assert response.json['message'] == 'El nombre de usuario ya existe'

def test_register_duplicate_email(client):
    """Prueba el registro con un correo electrónico que ya existe."""
    # Primero registrar un usuario
    client.post('/auth/register', json={
        'username': 'user1',
        'email': 'same@example.com',
        'password': 'password123',
        'phone': '1234567890'
    })
    
    # Intentar registrar otro usuario con el mismo correo electrónico
    response = client.post('/auth/register', json={
        'username': 'user2',
        'email': 'same@example.com',
        'password': 'password123',
        'phone': '0987654321'
    })
    
    assert response.status_code == 400
    assert 'message' in response.json
    assert response.json['message'] == 'El correo electrónico ya existe'

def test_login_success(client, admin_user):
    """Prueba el inicio de sesión exitoso."""
    response = client.post('/auth/login', json={
        'email': 'admin@example.com',
        'password': 'admin123'
    })
    
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'message' in response.json
    assert response.json['message'] == 'Login exitoso'

def test_login_invalid_credentials(client):
    """Prueba el inicio de sesión con credenciales inválidas."""
    response = client.post('/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
    assert 'message' in response.json
    assert response.json['message'] == 'Credenciales inválidas' 