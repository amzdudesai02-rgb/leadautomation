from flask import Blueprint, request, jsonify
from app.services.qa_service import QAService
from app.utils.error_handler import handle_error
from app.utils.auth_decorator import token_required

bp = Blueprint('qa', __name__)
qa_service = QAService()

@bp.route('/analyze', methods=['POST'])
@token_required
def analyze_qa(current_user):
    """Perform QA analysis on a brand"""
    try:
        data = request.get_json()
        
        if not data or 'brand_id' not in data:
            return jsonify({
                'success': False,
                'message': 'Brand ID is required'
            }), 400
        
        brand_id = data['brand_id']
        analysis = qa_service.analyze_brand(brand_id, current_user.id)
        
        return jsonify({
            'success': True,
            'message': 'QA analysis completed',
            'data': analysis
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/metrics/<brand_id>', methods=['GET'])
@token_required
def get_qa_metrics(brand_id, current_user):
    """Get QA metrics for a brand"""
    try:
        metrics = qa_service.get_metrics(brand_id)
        return jsonify({
            'success': True,
            'data': metrics
        }), 200
    except Exception as e:
        return handle_error(e)

