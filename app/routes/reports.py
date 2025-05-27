from flask import Blueprint, request, jsonify
from app.utils import require_auth, require_role
from app.controllers.report_controller import ReportController

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/sales", methods=["GET"])
@require_auth()
@require_role("admin")
def generate_sales_report():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    result, status_code = ReportController.generate_sales_report(start_date, end_date)
    return jsonify(result), status_code
