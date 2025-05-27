from datetime import datetime
from app.models import Appointment

messages = {
    "Unauthorized": "No autorizado",
    "Please provide start_date and end_date": "Por favor, proporcione start_date y end_date",
    "Invalid date format. Use YYYY-MM-DD": "Formato de fecha inválido. Use YYYY-MM-DD",
}


class ReportController:
    @staticmethod
    def generate_sales_report(start_date_str, end_date_str):
        if not start_date_str or not end_date_str:
            return {"message": messages["Please provide start_date and end_date"]}, 400

        try:
            start_date = (
                datetime.strptime(start_date_str, "%Y-%m-%d").date()
                if isinstance(start_date_str, str)
                else start_date_str
            )
            end_date = (
                datetime.strptime(end_date_str, "%Y-%m-%d").date()
                if isinstance(end_date_str, str)
                else end_date_str
            )
        except ValueError:
            return {"message": messages["Invalid date format. Use YYYY-MM-DD"]}, 400

        appointments = Appointment.query.filter(
            Appointment.date >= start_date,
            Appointment.date <= end_date,
            Appointment.status == "completed",  # Assuming 'completed' status for sales
        ).all()

        total_sales = sum(
            appointment.service.price
            for appointment in appointments
            if appointment.service
        )

        # Placeholder for exporting data
        # You can implement CSV or other export formats here

        return {"total_sales": total_sales}, 200
