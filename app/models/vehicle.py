from app import db
from datetime import datetime

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(20), unique=True, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.String(32), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at = db.Column(db.String(32), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), onupdate=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    owner = db.relationship('User', backref=db.backref('vehicles', lazy=True)) 