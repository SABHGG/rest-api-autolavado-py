from marshmallow import Schema, fields, validate
from app.schemas import ServiceSchema


class AppointmentServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    service_id = fields.Int(required=True)
    employee_id = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    service = fields.Nested(ServiceSchema, dump_only=True)


class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    status = fields.Str(
        validate=validate.OneOf(["pendiente", "en_progreso", "completada", "cancelada"])
    )
    user_id = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    services = fields.List(fields.Nested(AppointmentServiceSchema), required=False)
