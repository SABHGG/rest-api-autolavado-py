import enum
from app import db
from datetime import datetime, UTC

class RoleEnum(enum.Enum):
    admin = "admin"
    employee = "employee"
    client = "client"

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=RoleEnum.client.value)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def __init__(self, **kwargs):
        if 'role' in kwargs and isinstance(kwargs['role'], RoleEnum):
            kwargs['role'] = kwargs['role'].value
        super().__init__(**kwargs) 