from functools import wraps
from flask import request, jsonify
from app.services.auth_service import AuthService

def token_required(f):
    """Decorator to require authentication token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except:
                return jsonify({
                    'success': False,
                    'message': 'Invalid token format'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is missing'
            }), 401
        
        # Verify token
        user = AuthService.get_current_user(token)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token'
            }), 401
        
        # Add user to kwargs
        kwargs['current_user'] = user
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        user = kwargs.get('current_user')
        if not user or user.role != 'admin':
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        return f(*args, **kwargs)
    
    return decorated

def manager_required(f):
    """Decorator to require manager or admin role"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        user = kwargs.get('current_user')
        if not user or user.role not in ['admin', 'manager']:
            return jsonify({
                'success': False,
                'message': 'Manager access required'
            }), 403
        return f(*args, **kwargs)
    
    return decorated

