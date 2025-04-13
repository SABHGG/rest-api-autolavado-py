from flask import Blueprint, request, jsonify
from app import db
from app.models import Service
from app.schemas import ServiceSchema
from app.utils import require_auth, require_role

services_bp = Blueprint('services', __name__, url_prefix='/services')
service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)

@services_bp.route('/', methods=['POST'])
@require_auth()
@require_role('admin')
def create_service():
    data = request.get_json()
    errors = service_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    new_service = Service(
        name=data['name'],
        price=data['price']
    )
    db.session.add(new_service)
    db.session.commit()
    return service_schema.jsonify(new_service), 201

@services_bp.route('/', methods=['GET'])
@require_auth()
def get_services():
    services = Service.query.all()
    return services_schema.jsonify(services)