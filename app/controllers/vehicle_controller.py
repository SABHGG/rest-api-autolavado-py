from app import db
from app.models import Vehicle
from app.schemas import VehicleSchema

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)

class VehicleController:
    @staticmethod
    def register_vehicle(current_user_id, data):
        errors = vehicle_schema.validate(data)
        if errors:
            return errors, 400

        data['user_id'] = current_user_id  # Automatically assign the current user as the owner
        new_vehicle = Vehicle(**data)
        db.session.add(new_vehicle)
        db.session.commit()
        return vehicle_schema.dump(new_vehicle), 201

    @staticmethod
    def get_user_vehicles(user_id):
        # In a real app, you'd likely have role-based access control here
        vehicles = Vehicle.query.filter_by(user_id=user_id).all()
        return vehicles_schema.dump(vehicles) 