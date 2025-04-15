import pytest
from datetime import datetime, timedelta
from app.models import Appointment, Service
from app.models.user import RoleEnum, User
from app import db

@pytest.fixture
def service(app):
    """Crear un servicio para las pruebas."""
    with app.app_context():
        service = Service(name='Lavado Básico', price=50.00)
        db.session.add(service)
        db.session.commit()
        return service

@pytest.fixture
def employee_user(app):
    """Crear un usuario empleado para las pruebas."""
    with app.app_context():
        user = User(
            username='employee',
            email='employee@example.com',
            role=RoleEnum.employee
        )
        user.set_password('employee123')
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def employee_headers(client, employee_user):
    """Crear un token de autenticación para un empleado."""
    response = client.post('/login', json={
        'email': 'employee@example.com',
        'password': 'employee123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_create_appointment_success(client, auth_headers, client_user, service):
    """Prueba la creación exitosa de una cita."""
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    response = client.post('/appointments', json={
        'date': tomorrow,
        'time': '10:00',
        'service_id': service.id,
        'notes': 'Lavado con cera'
    }, headers=auth_headers)
    
    assert response.status_code == 201
    assert 'date' in response.json
    assert response.json['date'] == tomorrow
    assert response.json['time'] == '10:00'
    assert response.json['service_id'] == service.id
    assert response.json['notes'] == 'Lavado con cera'
    assert response.json['client_id'] == client_user.id
    
    # Verificar que la cita se creó en la base de datos
    with client.application.app_context():
        appointment = Appointment.query.filter_by(client_id=client_user.id).first()
        assert appointment is not None
        assert appointment.date.strftime('%Y-%m-%d') == tomorrow
        assert appointment.time == '10:00'
        assert appointment.service_id == service.id

def test_create_appointment_unauthorized(client, service):
    """Prueba la creación de una cita sin autenticación."""
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    response = client.post('/appointments', json={
        'date': tomorrow,
        'time': '10:00',
        'service_id': service.id,
        'notes': 'Lavado con cera'
    })
    
    assert response.status_code == 401

def test_get_appointment_success(client, auth_headers, client_user, service):
    """Prueba la obtención exitosa de una cita."""
    # Primero crear una cita
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    with client.application.app_context():
        appointment = Appointment(
            date=datetime.strptime(tomorrow, '%Y-%m-%d'),
            time='10:00',
            service_id=service.id,
            client_id=client_user.id,
            notes='Lavado con cera',
            status='pendiente'
        )
        db.session.add(appointment)
        db.session.commit()
        appointment_id = appointment.id
    
    response = client.get(f'/appointments/{appointment_id}', headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json['date'] == tomorrow
    assert response.json['time'] == '10:00'
    assert response.json['service_id'] == service.id
    assert response.json['client_id'] == client_user.id
    assert response.json['notes'] == 'Lavado con cera'
    assert response.json['status'] == 'pendiente'

def test_assign_appointment_success(client, auth_headers, client_user, service, employee_user):
    """Prueba la asignación exitosa de una cita a un empleado."""
    # Primero crear una cita
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    with client.application.app_context():
        appointment = Appointment(
            date=datetime.strptime(tomorrow, '%Y-%m-%d'),
            time='10:00',
            service_id=service.id,
            client_id=client_user.id,
            notes='Lavado con cera',
            status='pendiente'
        )
        db.session.add(appointment)
        db.session.commit()
        appointment_id = appointment.id
    
    response = client.put(f'/appointments/{appointment_id}/assign', json={
        'employee_id': employee_user.id
    }, headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json['employee_id'] == employee_user.id
    
    # Verificar que la cita se asignó correctamente en la base de datos
    with client.application.app_context():
        appointment = Appointment.query.get(appointment_id)
        assert appointment.employee_id == employee_user.id

def test_update_appointment_status_success(client, employee_headers, client_user, service, employee_user):
    """Prueba la actualización exitosa del estado de una cita."""
    # Primero crear una cita
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    with client.application.app_context():
        appointment = Appointment(
            date=datetime.strptime(tomorrow, '%Y-%m-%d'),
            time='10:00',
            service_id=service.id,
            client_id=client_user.id,
            employee_id=employee_user.id,
            notes='Lavado con cera',
            status='pendiente'
        )
        db.session.add(appointment)
        db.session.commit()
        appointment_id = appointment.id
    
    response = client.put(f'/appointments/{appointment_id}/status', json={
        'status': 'en_progreso'
    }, headers=employee_headers)
    
    assert response.status_code == 200
    assert response.json['status'] == 'en_progreso'
    
    # Verificar que el estado se actualizó correctamente en la base de datos
    with client.application.app_context():
        appointment = Appointment.query.get(appointment_id)
        assert appointment.status == 'en_progreso'

def test_cancel_appointment_success(client, auth_headers, client_user, service):
    """Prueba la cancelación exitosa de una cita."""
    # Primero crear una cita
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    with client.application.app_context():
        appointment = Appointment(
            date=datetime.strptime(tomorrow, '%Y-%m-%d'),
            time='10:00',
            service_id=service.id,
            client_id=client_user.id,
            notes='Lavado con cera',
            status='pendiente'
        )
        db.session.add(appointment)
        db.session.commit()
        appointment_id = appointment.id
    
    response = client.put(f'/appointments/{appointment_id}', json={
        'cancel': True
    }, headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json['message'] == 'Cita cancelada'
    
    # Verificar que la cita se eliminó de la base de datos
    with client.application.app_context():
        appointment = Appointment.query.get(appointment_id)
        assert appointment is None 