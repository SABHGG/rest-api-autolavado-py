from app import db
from datetime import datetime, timedelta
import enum


class AppointmentStatus(enum.Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    completada = "completada"
    cancelada = "cancelada"


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(
        db.String(10), db.ForeignKey("vehicles.plate"), nullable=False
    )
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        db.Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.pendiente
    )
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    vehicle = db.relationship("Vehicle", backref=db.backref("appointments", lazy=True))
    user = db.relationship("User", backref=db.backref("appointments", lazy=True))

    @property
    def end_time(self):
        return self.appointment_time + timedelta(minutes=30)
