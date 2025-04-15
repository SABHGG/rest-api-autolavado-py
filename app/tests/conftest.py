import pytest
from app import create_app
from app import db
from app.models.user import User, RoleEnum

@pytest.fixture
def app():
    """Crear una instancia de la aplicación para pruebas."""
    app = create_app('testing')
    
    # Crear todas las tablas en la base de datos de prueba
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Limpiar la base de datos después de las pruebas
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Crear un cliente de prueba."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Crear un runner de comandos de prueba."""
    return app.test_cli_runner()

@pytest.fixture
def auth_headers(client):
    """Crear un token de autenticación para las pruebas."""
    # Crear un usuario de prueba
    with client.application.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            role=RoleEnum.admin
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Obtener un token de autenticación
        response = client.post('/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        token = response.json['access_token']
        
        return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def admin_user(app):
    """Crear un usuario administrador para las pruebas."""
    with app.app_context():
        user = User(
            username='admin',
            email='admin@example.com',
            role=RoleEnum.admin
        )
        user.set_password('admin123')
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def client_user(app):
    """Crear un usuario cliente para las pruebas."""
    with app.app_context():
        user = User(
            username='client',
            email='client@example.com',
            role=RoleEnum.client
        )
        user.set_password('client123')
        db.session.add(user)
        db.session.commit()
        return user 