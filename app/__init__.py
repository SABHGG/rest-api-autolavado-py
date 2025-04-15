from flask import Flask, Blueprint, request, jsonify
from flask.json.provider import DefaultJSONProvider
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from app.config import get_config
from sqlalchemy import text
import json

db = SQLAlchemy()
jwt = JWTManager()

def init_db(app):
    with app.app_context():
        try:
            # Verificar conexión
            data = db.session.execute(text('SELECT 1'))
            print(f"✅ Conexión a la base de datos exitosa")
            # Importar los modelos
            from app.models import User, Vehicle, Service, Appointment, AppointmentService
            # Crear todas las tablas
            db.create_all()
        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {str(e)}")
            raise

def create_app(config_name=None):
    class CustomJSONProvider(DefaultJSONProvider):
        def dumps(self, obj, **kwargs):
            kwargs.setdefault("ensure_ascii", False)
            return json.dumps(obj, **kwargs)

        def loads(self, s, **kwargs):
            return json.loads(s, **kwargs)


    app = Flask(__name__)
    app.json_provider_class = CustomJSONProvider
    app.json = app.json_provider_class(app)
    # Cargar la configuración
    app.config.from_object(get_config(config_name))

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Inicializar la base de datos
    init_db(app)

    # Register blueprints
    register_blueprints(app)

    # Error handling for common errors (example)
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not Found', 'message': str(error)}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500
    
    return app

def register_blueprints(app):
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.vehicles import vehicles_bp
    from app.routes.appointments import appointments_bp
    from app.routes.services import services_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(vehicles_bp, url_prefix='/vehicles')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(reports_bp, url_prefix='/reports')

