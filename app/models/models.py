from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
import enum

db = SQLAlchemy()

class RoleEnum(enum.Enum):
    admin = "admin"
    employee = "employee"
    client = "client"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  
    phone = db.Column(db.String(10), unique=True, nullable=False)
    role = db.Column(Enum(RoleEnum), default=RoleEnum.client, nullable=False)
    
    vehicles = relationship("Vehicle", back_populates="user")
    appointments_as_client = relationship("Appointment", back_populates="client", foreign_keys="Appointment.client_id")
    appointments_as_employee = relationship("Appointment", back_populates="employee", foreign_keys="Appointment.employee_id")

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    type = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="vehicles")

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(Enum('pendiente', 'en_progreso', 'completada', 'cancelada', name='appointment_status'), default='pendiente')
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    client = relationship("User", back_populates="appointments_as_client", foreign_keys=[client_id])
    employee = relationship("User", back_populates="appointments_as_employee", foreign_keys=[employee_id])
    services = relationship("Service", secondary="appointment_services", back_populates="appointments")

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    appointments = relationship("Appointment", secondary="appointment_services", back_populates="services")

class AppointmentService(db.Model):
    __tablename__ = 'appointment_services'
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), primary_key=True)