from flask import jsonify
from app.utils.logger import get_logger

logger = get_logger(__name__)

def handle_error(error):
    """Handle errors and return JSON response"""
    logger.error(f"Error: {str(error)}")
    
    return jsonify({
        'success': False,
        'message': str(error),
        'error': type(error).__name__
    }), 500

