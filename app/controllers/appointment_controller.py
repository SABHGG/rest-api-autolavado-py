from flask import g, request
from app import db
from app.models import Appointment
from app.models.user import RoleEnum
from app.schemas import AppointmentSchema

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
    def get_appointment(appointment_id):
        appointment = Appointment.query.get_or_404(appointment_id)
        return appointment_schema.dump(appointment), 200

    @staticmethod
    def create_appointment():
        data = request.get_json()
        errors = appointment_schema.validate(data)
        if errors:
            return errors, 400

        appointment = appointment_schema.load(data)
        db.session.add(appointment)
        db.session.commit()

        return appointment_schema.dump(appointment), 201

    @staticmethod
    def assign_appointment(appointment_id):
        data = request.get_json()
        appointment = Appointment.query.get_or_404(appointment_id)

        if "employee_id" not in data:
            return {"message": message_translations["Missing employee_id"]}, 400

        appointment.employee_id = data["employee_id"]
        db.session.commit()

        # Placeholder for email notification
        # employee = User.query.get(data['employee_id'])
        # if employee:
        #     send_email(employee.email, "New Appointment Assigned", f"You have been assigned appointment {appointment_id}.")

        return appointment_schema.dump(appointment), 200

    @staticmethod
    def update_appointment_status(appointment_id, data):
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
    def update_appointment(appointment_id, data):
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
