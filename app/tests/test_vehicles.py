import pytest
from app.models import Vehicle
from app import db

def test_register_vehicle_success(client, auth_headers, client_user):
    """Prueba el registro exitoso de un vehículo."""
    response = client.post('/vehicles/', json={
        'brand': 'Toyota',
        'model': 'Corolla',
        'year': 2020,
        'color': 'Rojo',
        'plate': 'ABC123'
    }, headers=auth_headers)
    
    assert response.status_code == 201
    assert 'brand' in response.json
    assert response.json['brand'] == 'Toyota'
    assert response.json['model'] == 'Corolla'
    assert response.json['year'] == 2020
    assert response.json['color'] == 'Rojo'
    assert response.json['plate'] == 'ABC123'
    
    # Verificar que el vehículo se creó en la base de datos
    with client.application.app_context():
        vehicle = Vehicle.query.filter_by(plate='ABC123').first()
        assert vehicle is not None
        assert vehicle.brand == 'Toyota'
        assert vehicle.model == 'Corolla'

def test_register_vehicle_unauthorized(client):
    """Prueba el registro de un vehículo sin autenticación."""
    response = client.post('/vehicles/', json={
        'brand': 'Toyota',
        'model': 'Corolla',
        'year': 2020,
        'color': 'Rojo',
        'plate': 'ABC123'
    })
    
    assert response.status_code == 401

def test_get_user_vehicles_success(client, auth_headers, client_user):
    """Prueba la obtención exitosa de los vehículos de un usuario."""
    # Primero crear un vehículo
    with client.application.app_context():
        vehicle = Vehicle(
            brand='Toyota',
            model='Corolla',
            year=2020,
            color='Rojo',
            plate='ABC123',
            user_id=client_user.id
        )
        db.session.add(vehicle)
        db.session.commit()
    
    response = client.get('/vehicles/', headers=auth_headers)
    
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 1
    assert response.json[0]['brand'] == 'Toyota'
    assert response.json[0]['model'] == 'Corolla'

def test_get_user_vehicles_unauthorized(client):
    """Prueba la obtención de vehículos sin autenticación."""
    response = client.get('/vehicles/')
    
    assert response.status_code == 401 