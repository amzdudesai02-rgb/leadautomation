from flask import Blueprint, request, jsonify
from app.services.seller_service import SellerService
from app.utils.validators import validate_url
from app.utils.error_handler import handle_error
from app.utils.auth_decorator import token_required

bp = Blueprint('sellers', __name__)
seller_service = SellerService()

@bp.route('/', methods=['GET'])
@token_required
def get_sellers(current_user):
    """Get all sellers from database"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 50, type=int)
        status = request.args.get('status')
        validation_status = request.args.get('validation_status')
        search = request.args.get('search')
        
        filters = {}
        if status:
            filters['status'] = status
        if validation_status:
            filters['validation_status'] = validation_status
        if search:
            filters['search'] = search
        
        sellers = seller_service.get_all_sellers(page=page, limit=limit, filters=filters)
        return jsonify({
            'success': True,
            'data': sellers,
            'page': page,
            'limit': limit
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/<seller_id>', methods=['GET'])
@token_required
def get_seller(seller_id, current_user):
    """Get a specific seller by ID"""
    try:
        seller = seller_service.get_seller_by_id(seller_id)
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': seller
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/scrape', methods=['POST'])
@token_required
def scrape_seller(current_user):
    """Scrape seller information from Amazon"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'message': 'URL is required'
            }), 400
        
        url = data['url']
        
        # Validate URL
        if not validate_url(url):
            return jsonify({
                'success': False,
                'message': 'Invalid URL format'
            }), 400
        
        # Scrape seller data
        seller_data = seller_service.scrape_seller(url, current_user.id)
        
        return jsonify({
            'success': True,
            'message': 'Seller scraped successfully',
            'data': seller_data
        }), 201
        
    except Exception as e:
        return handle_error(e)

@bp.route('/<seller_id>', methods=['PUT'])
@token_required
def update_seller(seller_id, current_user):
    """Update seller information"""
    try:
        data = request.get_json()
        updated_seller = seller_service.update_seller(seller_id, data)
        
        return jsonify({
            'success': True,
            'message': 'Seller updated successfully',
            'data': updated_seller
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/<seller_id>', methods=['DELETE'])
@token_required
def delete_seller(seller_id, current_user):
    """Delete a seller"""
    try:
        seller_service.delete_seller(seller_id)
        return jsonify({
            'success': True,
            'message': 'Seller deleted successfully'
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/snipe', methods=['POST'])
@token_required
def snipe_seller(current_user):
    """
    Seller Sniping - 70% Automated
    Bot scrapes storefront, extracts brands, cross-checks database, adds to research queue
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'message': 'Seller URL is required'
            }), 400
        
        seller_url = data['url']
        auto_queue = data.get('auto_queue', True)  # Default to auto-queue
        
        # Validate URL
        if not validate_url(seller_url):
            return jsonify({
                'success': False,
                'message': 'Invalid URL format'
            }), 400
        
        # Run seller sniping automation
        result = seller_service.snipe_seller(seller_url, current_user.id, auto_queue=auto_queue)
        
        return jsonify({
            'success': True,
            'message': 'Seller sniping completed (70% Automated)',
            'data': result,
            'automation_percentage': result.get('automation_percentage', 70)
        }), 200
        
    except Exception as e:
        return handle_error(e)

