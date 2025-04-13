from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models.user import User, RoleEnum
from app.schemas import UserSchema

auth_bp = Blueprint('auth', __name__)

user_schema = UserSchema()

messages = {
    'Username already exists': 'El nombre de usuario ya existe',
    'Email already exists': 'El correo electrónico ya existe',
    'Default role not found': 'Rol predeterminado no encontrado',
    'User registered successfully': 'Usuario registrado exitosamente',
    'Invalid credentials': 'Credenciales inválidas'
}

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)
    

    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password,
        role=RoleEnum[data.get('role', 'client')]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': messages['User registered successfully']}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': messages['Invalid credentials']}), 401

    access_token = create_access_token(identity={'id': user.id, 'role': user.role.value})
    return jsonify({'access_token': access_token}), 200