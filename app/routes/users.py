from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app import db
from app.models.user import User, RoleEnum
from app.schemas import UserSchema
from app.utils import require_role, require_auth

users_bp = Blueprint('users', __name__, url_prefix='/users')
user_schema = UserSchema()
users_schema = UserSchema(many=True)

messages = {
    'Username or email already exists': 'El nombre de usuario o correo electrónico ya existe',
    'Invalid role ID': 'ID de rol inválido',
    'User not found': 'Usuario no encontrado',
    'Unauthorized': 'No autorizado',
    'Username already exists': 'El nombre de usuario ya existe',
    'Email already exists': 'El correo electrónico ya existe',
    'User deleted': 'Usuario eliminado'
}


@users_bp.route('/', methods=['POST'])
@require_auth()
@require_role("admin")
def create_user():
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    if User.query.filter_by(username=data['username']).first() or \
       User.query.filter_by(email=data['email']).first():
        return jsonify({'message': messages['Username or email already exists']}), 400

    try:
        role = RoleEnum[data.get('role', 'client')]  # Default to 'client' role
    except KeyError:
        role = RoleEnum.client

    user = User(username=data['username'], email=data['email'], password='', role=role)
    
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user), 201


@users_bp.route('/', methods=['GET'])
@require_auth()
@require_role("admin")
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)


@users_bp.route('/<int:user_id>', methods=['GET'])
@require_auth()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': messages['User not found']}), 404
    return user_schema.jsonify(user)


@users_bp.route('/<int:user_id>', methods=['PUT'])
@require_auth()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': messages['User not found']}), 404

    data = request.get_json()
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != RoleEnum.admin and user.id != current_user.id:
        return jsonify({'message': messages['Unauthorized']}), 403

    errors = user_schema.validate(data, partial=True)  # Allow partial updates
    if errors:
        return jsonify({'errors': errors}), 400

    if 'username' in data:
        if User.query.filter(User.username == data['username'], User.id != user.id).first():
            return jsonify({'message': messages['Username already exists']}), 400
        user.username = data['username']
    if 'email' in data:
        if User.query.filter(User.email == data['email'], User.id != user.id).first():
            return jsonify({'message': messages['Email already exists']}), 400
        user.email = data['email']
    if 'password' in data:
        user.set_password(data['password'])

    # Admin-only updates
    if current_user.role == RoleEnum.admin:
        if 'role' in data:
            user.role = RoleEnum[data['role']]
        if 'status' in data:
            user.status = data['status']

    db.session.commit()
    return user_schema.jsonify(user)


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@require_auth()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': messages['User not found']}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': messages['User deleted']})