from flask import Blueprint, request, jsonify
from app.services.brand_service import BrandService
from app.utils.error_handler import handle_error
from app.utils.auth_decorator import token_required

bp = Blueprint('brands', __name__)
brand_service = BrandService()

@bp.route('/', methods=['GET'])
@token_required
def get_brands(current_user):
    """Get all brands"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 50, type=int)
        status = request.args.get('status')
        search = request.args.get('search')
        
        filters = {}
        if status:
            filters['status'] = status
        if search:
            filters['search'] = search
        
        brands = brand_service.get_all_brands(page=page, limit=limit, filters=filters)
        return jsonify({
            'success': True,
            'data': brands,
            'page': page,
            'limit': limit
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/research', methods=['POST'])
@token_required
def research_brand(current_user):
    """Research brand information"""
    try:
        data = request.get_json()
        
        if not data or 'brand_name' not in data:
            return jsonify({
                'success': False,
                'message': 'Brand name is required'
            }), 400
        
        brand_name = data['brand_name']
        brand_data = brand_service.research_brand(brand_name, current_user.id)
        
        return jsonify({
            'success': True,
            'message': 'Brand researched successfully',
            'data': brand_data
        }), 201
    except Exception as e:
        return handle_error(e)

@bp.route('/<brand_id>', methods=['GET'])
@token_required
def get_brand(brand_id, current_user):
    """Get a specific brand by ID"""
    try:
        brand = brand_service.get_brand_by_id(brand_id)
        if not brand:
            return jsonify({
                'success': False,
                'message': 'Brand not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': brand
        }), 200
    except Exception as e:
        return handle_error(e)

