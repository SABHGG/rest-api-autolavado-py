from app import db
from datetime import datetime

class AppointmentService(db.Model):
    __tablename__ = 'appointment_services'
    
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    appointment = db.relationship('Appointment', backref=db.backref('appointment_services', lazy=True))
    service = db.relationship('Service', backref=db.backref('appointment_services', lazy=True)) 