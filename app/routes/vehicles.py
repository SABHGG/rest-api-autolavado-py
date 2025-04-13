from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.utils import require_auth
from app import db
from app.models import Vehicle
from app.schemas import VehicleSchema

vehicles_bp = Blueprint('vehicles', __name__)

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)


@vehicles_bp.route('/', methods=['POST'])
@require_auth()
def register_vehicle():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    errors = vehicle_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    data['user_id'] = current_user_id  # Automatically assign the current user as the owner
    new_vehicle = Vehicle(**data)
    db.session.add(new_vehicle)
    db.session.commit()
    return vehicle_schema.jsonify(new_vehicle), 201


@vehicles_bp.route('/user/<int:user_id>', methods=['GET'])
@require_auth()
def get_user_vehicles(user_id):
    # In a real app, you'd likely have role-based access control here
    vehicles = Vehicle.query.filter_by(user_id=user_id).all()
    return vehicles_schema.jsonify(vehicles)