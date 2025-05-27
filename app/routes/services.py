from flask import Blueprint, request, jsonify
from app.utils import require_auth, require_role
from app.controllers.service_controller import ServiceController

services_bp = Blueprint("services", __name__, url_prefix="/services")


@services_bp.route("/", methods=["POST"])
@require_auth()
@require_role("admin")
def create_service():
    data = request.get_json()
    result, status_code = ServiceController.create_service(data)
    return jsonify(result), status_code


@services_bp.route("/", methods=["GET"])
@require_auth()
def get_services():
    services = ServiceController.get_services()
    return jsonify(services)
