from marshmallow import Schema, fields, validate


class VehicleSchema(Schema):
    plate = fields.Str(required=True)
    brand = fields.Str(required=True)
    model = fields.Str(required=True)
    color = fields.Str(required=True)
    vehicle_type = fields.Function(
        serialize=lambda obj: obj.vehicle_type.value,
        deserialize=lambda value: value,
        required=True,
        validate=validate.OneOf(
            ["motocicleta", "coche", "camion", "autobus", "furgoneta"]
        ),
    )
    owner_id = fields.Str(required=False)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
