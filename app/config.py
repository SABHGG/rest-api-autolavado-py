import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()


class Config:
    """Configuración base de la aplicación."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    # Configuración base de PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""

    DEBUG = True
    # Usar la misma base de datos que en producción pero con prefijo dev_
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class ProductionConfig(Config):
    """Configuración para producción."""

    DEBUG = False
    def __init__(self):
        # Verificar que la URL de la base de datos esté configurada
        if not Config.SQLALCHEMY_DATABASE_URI:
            raise ValueError("DATABASE_URL debe estar configurada en producción")


class TestingConfig(Config):
    """Configuración para pruebas."""

    DEBUG = True
    TESTING = True
    # Usar SQLite en memoria para las pruebas
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    # Desactivar CSRF para las pruebas
    WTF_CSRF_ENABLED = False


# Diccionario para mapear entornos a configuraciones
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


# Obtener la configuración basada en el entorno
def get_config(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")
    return config.get(config_name, config["default"])
