from datetime import datetime
from marshmallow import Schema, fields, post_load, validate, validates, ValidationError
from app.schemas import ServiceSchema
from app.models import Appointment, AppointmentService


class AppointmentServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    service_id = fields.Int(required=True)
    employee_id = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    service = fields.Nested(ServiceSchema, dump_only=True)


class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    appointment_time = fields.DateTime(required=True)
    status = fields.Function(
        serialize=lambda obj: obj.status.value,
        deserialize=lambda value: value,
        required=True,
        validate=validate.OneOf(
            ["pendiente", "en_progreso", "completada", "cancelada"]
        ),
    )
    user_id = fields.Str(required=True)
    vehicle_id = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    services = fields.List(fields.Nested(AppointmentServiceSchema), required=True)

    @validates("appointment_time")
    def validate_appointment_time(self, value, *args, **kwargs):
        if value < datetime.now():
            raise ValidationError("La hora de la cita no puede ser en el pasado.")

    @post_load
    def make_appointment(self, data, **kwargs):
        services_data = data.pop("services", [])
        appointment = Appointment(**data)
        for s in services_data:
            service = AppointmentService(**s)
            appointment.appointment_services.append(service)
        return appointment
