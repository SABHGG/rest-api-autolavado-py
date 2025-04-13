import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    """Configuración base de la aplicación."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret')
    # Configuración base de PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    # Usar la misma base de datos que en producción pero con prefijo dev_
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/autolavado')

class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    # Para producción, requerimos la URL de la base de datos
    if not Config.SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL debe estar configurada en producción")

# Diccionario para mapear entornos a configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Obtener la configuración basada en el entorno
def get_config():
    env = os.getenv('FLASK_ENV', 'default')
    return config.get(env, config['default']) 