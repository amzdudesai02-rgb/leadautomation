"""
Health check and root routes
"""
from flask import Blueprint, jsonify
from app.models.database import db
from sqlalchemy import text

bp = Blueprint('health', __name__)

@bp.route('/health', methods=['GET'])
@bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    try:
        # Check database connection
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'message': 'API is running'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 503

@bp.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Lead Generation Tool API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'auth': '/api/auth',
            'sellers': '/api/sellers',
            'brands': '/api/brands',
            'qa': '/api/qa',
            'automation': '/api/automation'
        }
    }), 200

