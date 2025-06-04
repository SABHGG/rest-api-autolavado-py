from flask import Blueprint, jsonify
from app.utils import require_auth, require_role
from app.controllers.appointment_controller import AppointmentController

appointments_bp = Blueprint("appointments", __name__)


@appointments_bp.route("", methods=["GET"])
@require_auth()
def get_appointments():
    result, status_code = AppointmentController.get_appointments()
    return jsonify(result), status_code


@appointments_bp.route("", methods=["POST"])
@require_auth()
@require_role("client", "admin")
def create_appointment():
    result, status_code = AppointmentController.create_appointment()
    return jsonify(result), status_code


@appointments_bp.route("/<int:appointment_id>", methods=["GET"])
@require_auth()
def get_appointment(appointment_id):
    result, status_code = AppointmentController.get_appointment(appointment_id)
    return jsonify(result), status_code


@appointments_bp.route("/<int:appointment_id>/assign", methods=["PATCH"])
@require_auth()
@require_role("admin", "employee")
def assign_appointment(appointment_id):
    result, status_code = AppointmentController.assign_services_to_employee(
        appointment_id
    )
    return jsonify(result), status_code


@appointments_bp.route("/<int:appointment_id>/status", methods=["PATCH"])
@require_auth()
@require_role("admin", "employee")
def update_appointment_status(appointment_id):
    result, status_code = AppointmentController.update_appointment_status(
        appointment_id
    )
    return jsonify(result), status_code


@appointments_bp.route("/<int:appointment_id>", methods=["PUT"])
@require_auth()
@require_role("client", "admin", "employee")
def update_appointment(appointment_id):
    result, status_code = AppointmentController.update_appointment(appointment_id)
    return jsonify(result), status_code
