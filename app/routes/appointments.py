from flask import Blueprint, request, jsonify
from app.utils import require_auth, require_role
from app.controllers.appointment_controller import AppointmentController

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/appointments', methods=['POST'])
@require_auth()
@require_role('client')
def create_appointment():
    data = request.get_json()
    result, status_code = AppointmentController.create_appointment(data)
    return jsonify(result), status_code

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['GET'])
@require_auth()
def get_appointment(appointment_id):
    result, status_code = AppointmentController.get_appointment(appointment_id)
    return jsonify(result), status_code

@appointments_bp.route('/appointments/<int:appointment_id>/assign', methods=['PUT'])
@require_auth()
@require_role('admin')
def assign_appointment(appointment_id):
    data = request.get_json()
    result, status_code = AppointmentController.assign_appointment(appointment_id, data)
    return jsonify(result), status_code

@appointments_bp.route('/appointments/<int:appointment_id>/status', methods=['PUT'])
@require_auth()
@require_role('employee')
def update_appointment_status(appointment_id):
    data = request.get_json()
    result, status_code = AppointmentController.update_appointment_status(appointment_id, data)
    return jsonify(result), status_code

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
@require_auth()
@require_role('client')
def update_appointment(appointment_id):
    data = request.get_json()
    result, status_code = AppointmentController.update_appointment(appointment_id, data)
    return jsonify(result), status_code