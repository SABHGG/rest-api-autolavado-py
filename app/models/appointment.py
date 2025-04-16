from app import db
from datetime import datetime
import uuid

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(10), db.ForeignKey('vehicles.plate'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    vehicle = db.relationship('Vehicle', backref=db.backref('appointments', lazy=True))
    service = db.relationship('Service', backref=db.backref('appointments', lazy=True))
    user = db.relationship('User', backref=db.backref('appointments', lazy=True)) 