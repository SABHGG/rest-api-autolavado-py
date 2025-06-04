import pytest
from app import create_app, db
from sqlalchemy.orm import scoped_session, sessionmaker


@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture(scope="session")
def db_session(app):
    """Crear una conexión y transacción para toda la sesión de tests."""
    connection = db.engine.connect()
    transaction = connection.begin()

    # Crea un scoped_session manualmente usando sessionmaker
    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)

    # Reemplaza la sesión global de flask-sqlalchemy para que use esta
    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(scope="function")
def client(app, db_session):
    """Cliente para cada test (usa la sesión que abarca todos los tests)."""
    return app.test_client()
