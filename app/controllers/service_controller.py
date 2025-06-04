from app import db
from app.models import Service
from app.schemas import ServiceSchema
from app.utils import safe_controller

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)


class ServiceController:
    @staticmethod
    @safe_controller
    def create_service(data):
        errors = service_schema.validate(data)
        if errors:
            return errors, 400

        new_service = Service(
            name=data["name"],
            price=data["price"],
            description=data.get("description", ""),
            duration=data.get("duration"),
        )
        db.session.add(new_service)
        db.session.commit()
        return service_schema.dump(new_service), 201

    @staticmethod
    @safe_controller
    def get_services():
        services = Service.query.all()
        return services_schema.dump(services)
