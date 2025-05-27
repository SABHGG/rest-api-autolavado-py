from flask import Flask, jsonify
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import get_config
from sqlalchemy import text
import json

db = SQLAlchemy()
jwt = JWTManager()


def init_db(app):
    with app.app_context():
        try:
            # Verificar conexión
            db.session.execute(text("SELECT 1"))
            print("✅ Conexión a la base de datos exitosa")
            # Crear todas las tablas
            db.create_all()
        except Exception:
            print("❌ Error al inicializar la base de datos")
            raise


def create_app(config_name=None):
    class CustomJSONProvider(DefaultJSONProvider):
        def dumps(self, obj, **kwargs):
            kwargs.setdefault("ensure_ascii", False)
            return json.dumps(obj, **kwargs)

        def loads(self, s, **kwargs):
            return json.loads(s, **kwargs)

    app = Flask(__name__)
    CORS(app)
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
    SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI
    API_URL = "/static/swagger.yml"  # Our API spec
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
    )
    # Configure Swagger UI
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Error handling for common errors (example)
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": str(error)}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

    return app


def register_blueprints(app):
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.vehicles import vehicles_bp
    from app.routes.appointments import appointments_bp
    from app.routes.services import services_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(vehicles_bp, url_prefix="/vehicles")
    app.register_blueprint(appointments_bp, url_prefix="/appointments")
    app.register_blueprint(services_bp, url_prefix="/services")
    app.register_blueprint(reports_bp, url_prefix="/reports")
