# app/utils.py
import functools
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from app import db


# Middleware for authentication
def require_auth():
    def decorator(func):
        @functools.wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            g.current_user = user_id
            g.current_role = get_jwt().get("role")
            return func(*args, **kwargs)

        return wrapper

    return decorator


# Middleware for role-based authorization
def require_role(*required_role):
    def decorator(func):
        @functools.wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role")
            if role in required_role:
                return func(*args, **kwargs)

            return jsonify({"message": "Forbidden: Insufficient permissions"}), 403

        return wrapper

    return decorator


def safe_controller(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error", "details": str(e)}, 500
        except Exception as e:
            return {"message": "Unexpected error", "details": str(e)}, 500

    return wrapper


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
