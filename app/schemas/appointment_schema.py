from marshmallow import Schema, fields, validate
from app.schemas import ServiceSchema

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    status = fields.Str(validate=validate.OneOf(['pendiente', 'en_progreso', 'completada', 'cancelada']))
    client_id = fields.Int(required=True)
    employee_id = fields.Int()
    services = fields.List(fields.Nested(ServiceSchema, dump_only=True))