from flask import g, request
from marshmallow import ValidationError
from app import db
from app.models import Appointment, AppointmentService
from app.models.user import RoleEnum
from app.schemas import AppointmentSchema
from app.utils import safe_controller

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

message_translations = {
    "Unauthorized": "No autorizado",
    "Missing employee_id": "Falta employee_id",
    "Invalid status": "Estado inválido",
    "Appointment canceled": "Cita cancelada",
}


class AppointmentController:
    @staticmethod
    @safe_controller
    def get_appointments():
        MAX_LIMIT = 50
        limit = min(request.args.get("limit", 10, type=int), MAX_LIMIT)
        offset = request.args.get("offset", 0, type=int)
        status = request.args.get("status", type=str)

        if g.current_role == RoleEnum.client:
            appointments = (
                Appointment.query.filter_by(user_id=g.current_user.id, status=status)
                .offset(offset)
                .limit(limit)
                .all()
            )
        elif g.current_role == RoleEnum.employee:
            appointments = (
                Appointment.query.filter_by(
                    employee_id=g.current_user.id, status=status
                )
                .offset(offset)
                .limit(limit)
                .all()
            )
        else:
            appointments = Appointment.query.offset(offset).limit(limit).all()

        return appointments_schema.dump(appointments), 200

    @staticmethod
    @safe_controller
    def get_appointment(appointment_id):
        appointment = Appointment.query.get_or_404(appointment_id)
        return appointment_schema.dump(appointment), 200

    @staticmethod
    @safe_controller
    def create_appointment():
        data = request.get_json()
        data["user_id"] = g.current_user

        errors = appointment_schema.validate(data)
        if errors:
            return errors, 400

        try:
            appointment = appointment_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        db.session.add(appointment)
        db.session.commit()
        return appointment_schema.dump(appointment), 201

    @staticmethod
    @safe_controller
    def assign_services_to_employee(appointment_id):
        # Obtener todos los servicios de la cita
        services = AppointmentService.query.filter_by(
            appointment_id=appointment_id
        ).all()

        if not services:
            return {"message": "Appointment or services not found"}, 404

        already_assigned = [s for s in services if s.employee_id is not None]
        if already_assigned:
            return {"message": "Some or all services are already assigned"}, 400

        # Asignar al empleado actual
        for service in services:
            service.employee_id = g.current_user

        db.session.commit()

        return {"message": "Services assigned successfully"}, 200

    @staticmethod
    @safe_controller
    def update_appointment_status(appointment_id):
        data = request.get_json()
        appointment = Appointment.query.get_or_404(appointment_id)

        status_translations = {
            "pending": "pendiente",
            "in_progress": "en_progreso",
            "completed": "completada",
        }
        valid_statuses = list(status_translations.values())
        if "status" not in data or data["status"] not in valid_statuses:
            return {"message": message_translations["Invalid status"]}, 400

        appointment.status = data["status"]
        db.session.commit()

        return appointment_schema.dump(appointment), 200

    @staticmethod
    @safe_controller
    def update_appointment(appointment_id, data):
        data = request.get_json()
        appointment = Appointment.query.get_or_404(appointment_id)

        if data.get("status") == "cancelada":
            db.session.delete(appointment)
            db.session.commit()
            return {"message": message_translations["Appointment canceled"]}, 200

        errors = appointment_schema.validate(data, partial=True)
        if errors:
            return errors, 400

        updated_appointment = appointment_schema.load(
            data, instance=appointment, session=db.session, partial=True
        )
        db.session.commit()

        return appointment_schema.dump(updated_appointment), 200
