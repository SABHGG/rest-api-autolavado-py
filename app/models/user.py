import enum
from app import db
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

class RoleEnum(enum.Enum):
    admin = "admin"
    employee = "employee"
    client = "client"

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(162) , nullable=False)
    role = db.Column(db.String(20), nullable=False, default=RoleEnum.client.value)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, **kwargs):
        if 'role' in kwargs and isinstance(kwargs['role'], RoleEnum):
            kwargs['role'] = kwargs['role'].value
        super().__init__(**kwargs)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)