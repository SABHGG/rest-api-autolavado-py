from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Appointment, User
from app.models.user import RoleEnum
from app.schemas import AppointmentSchema
from app.utils import require_auth, require_role

appointments_bp = Blueprint('appointments', __name__)

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

message_translations = {
    'Unauthorized': 'No autorizado',
    'Missing employee_id': 'Falta employee_id',
    'Invalid status': 'Estado inválido',
    'Appointment canceled': 'Cita cancelada'
}


@appointments_bp.route('/appointments', methods=['POST'])
@require_auth()
@require_role('client')
def create_appointment():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    data['client_id'] = current_user_id  # Automatically assign the client ID
    
    errors = appointment_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_appointment = appointment_schema.load(data, session=db.session)
    db.session.add(new_appointment)
    db.session.commit()

    # Placeholder for email reminder
    # send_email(new_appointment.client.email, "Appointment Confirmation", "Your appointment has been requested.")

    return appointment_schema.dump(new_appointment), 201


@appointments_bp.route('/appointments/<int:appointment_id>', methods=['GET'])
@require_auth()
def get_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role == RoleEnum.client and appointment.client_id != current_user_id:
        return jsonify({'message': message_translations['Unauthorized']}), 403
    if current_user.role == RoleEnum.employee and appointment.employee_id != current_user_id:
        return jsonify({'message': message_translations['Unauthorized']}), 403

    return appointment_schema.dump(appointment), 200


@appointments_bp.route('/appointments/<int:appointment_id>/assign', methods=['PUT'])
@require_auth()
@require_role('admin')
def assign_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.get_json()

    if 'employee_id' not in data:
        return jsonify({'message': message_translations['Missing employee_id']}), 400

    appointment.employee_id = data['employee_id']
    db.session.commit()

    # Placeholder for email notification
    # employee = User.query.get(data['employee_id'])
    # if employee:
    #     send_email(employee.email, "New Appointment Assigned", f"You have been assigned appointment {appointment_id}.")

    return appointment_schema.dump(appointment), 200


@appointments_bp.route('/appointments/<int:appointment_id>/status', methods=['PUT'])
@require_auth()
@require_role('employee')
def update_appointment_status(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    current_user_id = get_jwt_identity()

    if appointment.employee_id != current_user_id:
        return jsonify({'message': message_translations['Unauthorized']}), 403
    
    data = request.get_json()
    status_translations = {'pending': 'pendiente', 'in_progress': 'en_progreso', 'completed': 'completada'}
    valid_statuses = list(status_translations.values())
    if 'status' not in data or data['status'] not in valid_statuses:
        return jsonify({'message': message_translations['Invalid status']}), 400

    appointment.status = data['status']
    db.session.commit()

    return appointment_schema.dump(appointment), 200


@appointments_bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
@require_auth()
@require_role('client')
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    current_user_id = get_jwt_identity()
    
    if appointment.client_id != current_user_id:
        return jsonify({'message': message_translations['Unauthorized']}), 403

    data = request.get_json()
    if 'cancel' in data and data['cancel'] == True:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': message_translations['Appointment canceled']}), 200

    errors = appointment_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    updated_appointment = appointment_schema.load(data, instance=appointment, session=db.session, partial=True)
    db.session.commit()
    
    return appointment_schema.dump(updated_appointment), 200