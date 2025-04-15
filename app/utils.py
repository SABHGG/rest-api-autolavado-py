# app/utils.py
import functools
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import jsonify, g


# Middleware for authentication
def require_auth():
    def decorator(func):
        @functools.wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            g.current_user = user_id
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Middleware for role-based authorization
def require_role(required_role):
    def decorator(func):
        @functools.wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role")
            if role == required_role:
                return func(*args, **kwargs)
            return jsonify({"message": "Forbidden: Insufficient permissions"}), 403
        return wrapper
    return decorator

def send_email(to, subject, body):
    """
    Placeholder function for sending emails.
    In a real application, this would use a library like smtplib or a service like SendGrid.
    """
    print(f"Sending email to: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    # In a real implementation:
    # - Configure SMTP settings (host, port, credentials).
    # - Create an email message object.
    # - Send the email.
    return True  # Indicate success for now