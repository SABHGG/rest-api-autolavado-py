from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from app.config import get_config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Cargar la configuración
    app.config.from_object(get_config())

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

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

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        try:
            # Importar los modelos
            from app.models import User, Vehicle, Service, Appointment, AppointmentService
            # Crear todas las tablas
            db.create_all()
            print("¡Tablas creadas exitosamente!")
        except Exception as e:
            print(f"Error al crear las tablas: {str(e)}")
    app.run(debug=True)