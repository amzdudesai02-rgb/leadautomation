import jwt
from datetime import datetime, timedelta
from app.models.database import db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.config import Config
from app.utils.logger import get_logger
from flask import request

logger = get_logger(__name__)

class AuthService:
    """Authentication service"""
    
    @staticmethod
    def generate_token(user_id, username, role):
        """Generate JWT token"""
        try:
            payload = {
                'user_id': user_id,
                'username': username,
                'role': role,
                'exp': datetime.utcnow() + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
            return token
        except Exception as e:
            logger.error(f"Error generating token: {str(e)}")
            return None
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
    
    @staticmethod
    def register_user(username, email, password, full_name=None, role='user'):
        """Register a new user"""
        try:
            # Check if user already exists
            if User.query.filter_by(username=username).first():
                return {'success': False, 'message': 'Username already exists'}
            
            if User.query.filter_by(email=email).first():
                return {'success': False, 'message': 'Email already exists'}
            
            # Create new user
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                role=role
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # Log registration
            AuthService._log_action(user.id, 'register', 'user', user.id, 'User registered')
            
            logger.info(f"User registered: {username}")
            return {
                'success': True,
                'message': 'User registered successfully',
                'user': user.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error registering user: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    @staticmethod
    def login_user(username, password):
        """Login user"""
        try:
            # Find user by username or email
            user = User.query.filter(
                (User.username == username) | (User.email == username)
            ).first()
            
            if not user:
                return {'success': False, 'message': 'Invalid username or password'}
            
            if not user.is_active:
                return {'success': False, 'message': 'Account is deactivated'}
            
            if not user.check_password(password):
                return {'success': False, 'message': 'Invalid username or password'}
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Generate token
            token = AuthService.generate_token(user.id, user.username, user.role)
            
            if not token:
                return {'success': False, 'message': 'Failed to generate token'}
            
            # Log login
            AuthService._log_action(user.id, 'login', 'user', user.id, 'User logged in', request)
            
            logger.info(f"User logged in: {username}")
            return {
                'success': True,
                'message': 'Login successful',
                'token': token,
                'user': user.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error logging in user: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    @staticmethod
    def get_current_user(token):
        """Get current user from token"""
        try:
            payload = AuthService.verify_token(token)
            if not payload:
                return None
            
            user = User.query.get(payload.get('user_id'))
            return user
            
        except Exception as e:
            logger.error(f"Error getting current user: {str(e)}")
            return None
    
    @staticmethod
    def _log_action(user_id, action, entity_type, entity_id, description, request_obj=None):
        """Log user action to audit log"""
        try:
            log = AuditLog(
                user_id=user_id,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                description=description,
                ip_address=request_obj.remote_addr if request_obj else None,
                user_agent=request_obj.headers.get('User-Agent') if request_obj else None
            )
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            logger.error(f"Error logging action: {str(e)}")

