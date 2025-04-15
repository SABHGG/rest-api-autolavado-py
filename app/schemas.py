from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    phone = fields.Str(required=True, validate=validate.Length(min=10, max=10))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    

class VehicleSchema(Schema):
    id = fields.Int(dump_only=True)
    license_plate = fields.Str(required=True)
    type = fields.Str()
    user_id = fields.Int(required=True)

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    status = fields.Str(validate=validate.OneOf(['pendiente', 'en_progreso', 'completada', 'cancelada']))
    client_id = fields.Int(required=True)  # Assuming this remains as client_id
    employee_id = fields.Int()
    services = fields.List(fields.Nested('ServiceSchema', dump_only=True))

class ServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)