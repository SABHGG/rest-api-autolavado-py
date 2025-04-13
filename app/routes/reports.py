from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Appointment
from app import db
from datetime import datetime, date

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/sales', methods=['GET'])
@jwt_required()
def generate_sales_report():
    messages = {
        'Unauthorized': 'No autorizado',
        'Please provide start_date and end_date': 'Por favor, proporcione start_date y end_date',
        'Invalid date format. Use YYYY-MM-DD': 'Formato de fecha inválido. Use YYYY-MM-DD'
    }
    current_user_id = get_jwt_identity()
    # Assuming get_jwt_identity returns user ID, we need to fetch user details
    user = db.session.query(db.User).get(current_user_id)
    if user.role.name != 'admin':
        return jsonify({'message': messages['Unauthorized']}), 403

    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    if not start_date_str or not end_date_str:
        return jsonify({'message': messages['Please provide start_date and end_date']}), 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if isinstance(start_date_str, str) else start_date_str
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if isinstance(end_date_str, str) else end_date_str
    except ValueError:
        return jsonify({'message': messages['Invalid date format. Use YYYY-MM-DD']}), 400

    appointments = Appointment.query.filter(
        Appointment.date >= start_date,
        Appointment.date <= end_date,
        Appointment.status == 'completed'  # Assuming 'completed' status for sales
    ).all()

    total_sales = sum(appointment.service.price for appointment in appointments if appointment.service)

    # Placeholder for exporting data
    # You can implement CSV or other export formats here

    return jsonify({'total_sales': total_sales})