from app import db
from datetime import datetime
import uuid

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.String(32), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at = db.Column(db.String(32), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), onupdate=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    vehicle = db.relationship('Vehicle', backref=db.backref('appointments', lazy=True))
    service = db.relationship('Service', backref=db.backref('appointments', lazy=True))
    user = db.relationship('User', backref=db.backref('appointments', lazy=True)) 