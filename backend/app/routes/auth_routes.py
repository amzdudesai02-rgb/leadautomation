from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.utils.error_handler import handle_error
from app.utils.auth_decorator import token_required

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        
        if not username or not email or not password:
            return jsonify({
                'success': False,
                'message': 'Username, email, and password are required'
            }), 400
        
        result = AuthService.register_user(username, email, password, full_name)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return handle_error(e)

@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        result = AuthService.login_user(username, password)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return handle_error(e)

@bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current user information"""
    try:
        return jsonify({
            'success': True,
            'data': current_user.to_dict()
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Logout user"""
    try:
        # Log logout action
        from app.models.audit_log import AuditLog
        from app.models.database import db
        from flask import request as req
        
        log = AuditLog(
            user_id=current_user.id,
            action='logout',
            entity_type='user',
            entity_id=current_user.id,
            description='User logged out',
            ip_address=req.remote_addr,
            user_agent=req.headers.get('User-Agent')
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
    except Exception as e:
        return handle_error(e)

