from app import db
from datetime import datetime
import enum


class VehicleType(enum.Enum):
    motocicleta = "motocicleta"
    coche = "coche"
    camion = "camion"
    autobus = "autobus"
    furgoneta = "furgoneta"


class Vehicle(db.Model):
    __tablename__ = "vehicles"
    plate = db.Column(db.String(10), primary_key=True, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    vehicle_type = db.Column(db.Enum(VehicleType), nullable=False)

    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    owner = db.relationship("User", backref=db.backref("vehicles", lazy=True))
