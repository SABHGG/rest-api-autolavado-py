from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models.user import User, RoleEnum
from app.schemas import UserSchema

user_schema = UserSchema()

messages = {
    "Username already exists": "El nombre de usuario ya existe",
    "Email already exists": "El correo electrónico ya existe",
    "Default role not found": "Rol predeterminado no encontrado",
    "User registered successfully": "Usuario registrado exitosamente",
    "Invalid credentials": "Credenciales inválidas",
    "Phone already exists": "El número de teléfono ya existe",
}


class AuthController:
    @staticmethod
    def register(data):
        errors = user_schema.validate(data)
        if errors:
            return {"errors": errors}, 400

        if User.query.filter_by(username=data["username"]).first():
            return {"message": messages["Username already exists"]}, 400

        if User.query.filter_by(email=data["email"]).first():
            return {"message": messages["Email already exists"]}, 400

        if User.query.filter_by(phone=data["phone"]).first():
            return {"message": messages["Phone already exists"]}, 400

        hashed_password = generate_password_hash(data["password"])

        new_user = User(
            username=data["username"],
            email=data["email"],
            phone=data["phone"],
            password_hash=hashed_password,
            role=RoleEnum.client.value,
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": messages["User registered successfully"]}, 201

    @staticmethod
    def login(data):
        user = User.query.filter_by(email=data["email"]).first()

        if not user or not check_password_hash(user.password_hash, data["password"]):
            return {"message": messages["Invalid credentials"]}, 401

        access_token = create_access_token(
            identity=str(user.id), additional_claims={"role": user.role}
        )
        return {"message": "Login exitoso", "access_token": access_token}, 200
