from marshmallow import Schema, fields

class VehicleSchema(Schema):
    id = fields.Int(dump_only=True)
    license_plate = fields.Str(required=True)
    type = fields.Str()
    user_id = fields.Int(required=True)