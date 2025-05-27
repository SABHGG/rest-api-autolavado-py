from app import db
from app.models import Vehicle
from app.schemas import VehicleSchema
from flask import request
from flask_jwt_extended import get_jwt_identity

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)


class VehicleController:
    @staticmethod
    def register_vehicle():
        current_user_id = get_jwt_identity()
        data = request.get_json()

        errors = vehicle_schema.validate(data)
        if errors:
            return errors, 400

        data["owner_id"] = (
            current_user_id  # Automatically assign the current user as the owner
        )
        new_vehicle = Vehicle(**data)
        db.session.add(new_vehicle)
        db.session.commit()
        return vehicle_schema.dump(new_vehicle), 201

    @staticmethod
    def get_user_vehicles():
        user_id = get_jwt_identity()
        vehicles = Vehicle.query.filter_by(owner_id=user_id).all()
        return vehicles_schema.dump(vehicles)
