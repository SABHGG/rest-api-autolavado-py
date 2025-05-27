from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    result, status_code = AuthController.register(data)
    print(result)
    print(status_code)
    return jsonify(result), status_code


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    result, status_code = AuthController.login(data)
    return jsonify(result), status_code
