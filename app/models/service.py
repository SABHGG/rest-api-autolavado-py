from app import db
from datetime import datetime

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=30)  # duración en minutos, por defecto 30 minutos
    created_at = db.Column(db.String(32), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at = db.Column(db.String(32), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), onupdate=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))