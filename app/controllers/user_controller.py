from flask import g
from app import db
from app.models.user import User, RoleEnum
from app.schemas import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

messages = {
    "Username or email already exists": "El nombre de usuario o correo electrónico ya existe",
    "Invalid role ID": "ID de rol inválido",
    "User not found": "Usuario no encontrado",
    "Unauthorized": "No autorizado",
    "Username already exists": "El nombre de usuario ya existe",
    "Email already exists": "El correo electrónico ya existe",
    "User deleted": "Usuario eliminado",
}


class UserController:
    @staticmethod
    def create_user(data):
        try:
            errors = user_schema.validate(data)
            if errors:
                return {"errors": errors}, 400

            if (
                User.query.filter_by(username=data["username"]).first()
                or User.query.filter_by(email=data["email"]).first()
            ):
                return {"message": messages["Username or email already exists"]}, 400

            try:
                role = RoleEnum[data.get("role", "client")]
            except KeyError:
                role = RoleEnum.client

            user = User(
                username=data["username"],
                email=data["email"],
                phone=data["phone"],
                password="",
                role=role,
            )
            user.set_password(data["password"])
            db.session.add(user)
            db.session.commit()

            return user_schema.dump(user), 201
        except Exception:
            return {"message": "Algo salio mal"}, 500

    @staticmethod
    def get_all_users():
        users = User.query.all()
        return users_schema.dump(users)

    @staticmethod
    def get_user():
        user_id = g.current_user
        if not user_id:
            return {"message": messages["User not found"]}, 404

        user = User.query.get(user_id)
        return user_schema.dump(user)

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return {"message": messages["User not found"]}, 404

        current_user_id = g.current_user
        current_user = User.query.get(current_user_id)

        if current_user.role != RoleEnum.admin and user.id != current_user.id:
            return {"message": messages["Unauthorized"]}, 403

        errors = user_schema.validate(data, partial=True)
        if errors:
            return {"errors": errors}, 400

        if "username" in data:
            if User.query.filter(
                User.username == data["username"], User.id != user.id
            ).first():
                return {"message": messages["Username already exists"]}, 400
            user.username = data["username"]
        if "email" in data:
            if User.query.filter(
                User.email == data["email"], User.id != user.id
            ).first():
                return {"message": messages["Email already exists"]}, 400
            user.email = data["email"]
        if "password" in data:
            user.set_password(data["password"])

        if current_user.role == RoleEnum.admin:
            if "role" in data:
                user.role = RoleEnum[data["role"]]
            if "status" in data:
                user.status = data["status"]

        db.session.commit()
        return user_schema.dump(user)

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": messages["User not found"]}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": messages["User deleted"]}
