from flask import Blueprint, jsonify

from app.controllers.vehicle_controller import VehicleController
from app.utils import require_auth

vehicles_bp = Blueprint("vehicles", __name__)


@vehicles_bp.route("/", methods=["POST"])
@require_auth()
def register_vehicle():
    result, status_code = VehicleController.register_vehicle()
    return jsonify(result), status_code


@vehicles_bp.route("/", methods=["GET"])
@require_auth()
def get_user_vehicles():
    vehicles = VehicleController.get_user_vehicles()
    return jsonify(vehicles)
