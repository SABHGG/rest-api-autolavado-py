from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.report_controller import ReportController

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/sales', methods=['GET'])
@jwt_required()
def generate_sales_report():
    current_user_id = get_jwt_identity()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    result, status_code = ReportController.generate_sales_report(current_user_id, start_date, end_date)
    return jsonify(result), status_code