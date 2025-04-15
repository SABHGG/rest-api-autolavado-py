from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.utils import require_auth
from app.controllers.vehicle_controller import VehicleController

vehicles_bp = Blueprint('vehicles', __name__)

@vehicles_bp.route('/', methods=['POST'])
@require_auth()
def register_vehicle():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    result, status_code = VehicleController.register_vehicle(current_user_id, data)
    return jsonify(result), status_code

@vehicles_bp.route('/', methods=['GET'])
@require_auth()
def get_user_vehicles():
    current_user_id = get_jwt_identity()
    vehicles = VehicleController.get_user_vehicles(current_user_id)
    return jsonify(vehicles)