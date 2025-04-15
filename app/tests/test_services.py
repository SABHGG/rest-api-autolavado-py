import pytest
from app.models import Service
from app import db

def test_create_service_success(client, auth_headers, admin_user):
    """Prueba la creación exitosa de un servicio por un administrador."""
    response = client.post('/services/', json={
        'name': 'Lavado Premium',
        'price': 150.00
    }, headers=auth_headers)
    
    assert response.status_code == 201
    assert 'name' in response.json
    assert response.json['name'] == 'Lavado Premium'
    assert response.json['price'] == 150.00
    
    # Verificar que el servicio se creó en la base de datos
    with client.application.app_context():
        service = Service.query.filter_by(name='Lavado Premium').first()
        assert service is not None
        assert service.price == 150.00

def test_create_service_unauthorized(client):
    """Prueba la creación de un servicio sin autenticación."""
    response = client.post('/services/', json={
        'name': 'Lavado Premium',
        'price': 150.00
    })
    
    assert response.status_code == 401

def test_create_service_forbidden(client, auth_headers, client_user):
    """Prueba la creación de un servicio por un usuario no administrador."""
    # Crear un token para un usuario cliente
    with client.application.app_context():
        response = client.post('/login', json={
            'email': 'client@example.com',
            'password': 'client123'
        })
        client_token = response.json['access_token']
        client_headers = {'Authorization': f'Bearer {client_token}'}
    
    response = client.post('/services/', json={
        'name': 'Lavado Premium',
        'price': 150.00
    }, headers=client_headers)
    
    assert response.status_code == 403

def test_get_services_success(client, auth_headers):
    """Prueba la obtención exitosa de todos los servicios."""
    # Primero crear un servicio
    with client.application.app_context():
        service = Service(name='Lavado Básico', price=50.00)
        db.session.add(service)
        db.session.commit()
    
    response = client.get('/services/', headers=auth_headers)
    
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'Lavado Básico'
    assert response.json[0]['price'] == 50.00

def test_get_services_unauthorized(client):
    """Prueba la obtención de servicios sin autenticación."""
    response = client.get('/services/')
    
    assert response.status_code == 401 