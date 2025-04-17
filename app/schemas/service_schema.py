from marshmallow import Schema, fields

class ServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=False)
    duration = fields.Int(required=False)