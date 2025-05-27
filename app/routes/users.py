from flask import Blueprint, request, jsonify
from app.utils import require_role, require_auth
from app.controllers.user_controller import UserController

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/", methods=["POST"])
@require_auth()
@require_role("admin")
def create_user():
    data = request.get_json()
    result, status_code = UserController.create_user(data)
    return jsonify(result), status_code


@users_bp.route("/", methods=["GET"])
@require_auth()
@require_role("admin")
def get_users():
    users = UserController.get_all_users()
    return jsonify(users)


@users_bp.route("", methods=["GET"])
@require_auth()
def get_user():
    result = UserController.get_user()
    return jsonify(result)


@users_bp.route("/<string:user_id>", methods=["PUT"])
@require_auth()
def update_user(user_id):
    data = request.get_json()
    result = UserController.update_user(user_id, data)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)


@users_bp.route("/<string:user_id>", methods=["DELETE"])
@require_auth()
def delete_user(user_id):
    result, status_code = UserController.delete_user(user_id)
    return jsonify(result), status_code
