from app.models.database import db
from app.models.seller import Seller
from app.models.brand import Brand
from app.models.qa_analysis import QAAnalysis
from app.utils.logger import get_logger
from sqlalchemy import desc, or_
from datetime import datetime

logger = get_logger(__name__)

class DatabaseService:
    """Service for database operations (replaces Google Sheets)"""
    
    # Seller operations
    @staticmethod
    def get_sellers(page=1, limit=50, filters=None):
        """Get sellers with pagination"""
        try:
            query = Seller.query
            
            # Apply filters
            if filters:
                if filters.get('status'):
                    query = query.filter(Seller.status == filters['status'])
                if filters.get('validation_status'):
                    query = query.filter(Seller.validation_status == filters['validation_status'])
                if filters.get('is_duplicate') is not None:
                    query = query.filter(Seller.is_duplicate == filters['is_duplicate'])
                if filters.get('search'):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            Seller.name.ilike(search_term),
                            Seller.email.ilike(search_term),
                            Seller.company_name.ilike(search_term)
                        )
                    )
            
            # Pagination
            total = query.count()
            sellers = query.order_by(desc(Seller.created_at)).offset((page - 1) * limit).limit(limit).all()
            
            return {
                'data': [seller.to_dict() for seller in sellers],
                'total': total,
                'page': page,
                'limit': limit,
                'pages': (total + limit - 1) // limit
            }
        except Exception as e:
            logger.error(f"Error getting sellers: {str(e)}")
            return {'data': [], 'total': 0, 'page': page, 'limit': limit, 'pages': 0}
    
    @staticmethod
    def get_seller_by_id(seller_id):
        """Get seller by ID"""
        try:
            seller = Seller.query.get(seller_id)
            return seller.to_dict() if seller else None
        except Exception as e:
            logger.error(f"Error getting seller: {str(e)}")
            return None
    
    @staticmethod
    def save_seller(seller_data, user_id=None):
        """Save seller to database"""
        try:
            seller = Seller(
                name=seller_data.get('name', ''),
                email=seller_data.get('email', ''),
                store_url=seller_data.get('store_url', ''),
                phone=seller_data.get('phone', ''),
                company_name=seller_data.get('company_name', ''),
                location=seller_data.get('location', ''),
                rating=seller_data.get('rating'),
                total_reviews=seller_data.get('total_reviews', 0),
                status=seller_data.get('status', 'active'),
                is_duplicate=seller_data.get('is_duplicate', False),
                validation_status=seller_data.get('validation_status', 'pending'),
                validation_issues=seller_data.get('validation_issues'),
                notes=seller_data.get('notes', ''),
                created_by=user_id
            )
            
            db.session.add(seller)
            db.session.commit()
            
            logger.info(f"Seller saved: {seller.id}")
            return seller.to_dict()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving seller: {str(e)}")
            raise
    
    @staticmethod
    def update_seller(seller_id, seller_data):
        """Update seller"""
        try:
            seller = Seller.query.get(seller_id)
            if not seller:
                return None
            
            # Update fields
            for key, value in seller_data.items():
                if hasattr(seller, key) and key not in ['id', 'created_at', 'created_by']:
                    setattr(seller, key, value)
            
            seller.updated_at = datetime.utcnow()
            db.session.commit()
            
            return seller.to_dict()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating seller: {str(e)}")
            raise
    
    @staticmethod
    def delete_seller(seller_id):
        """Delete seller"""
        try:
            seller = Seller.query.get(seller_id)
            if seller:
                db.session.delete(seller)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting seller: {str(e)}")
            raise
    
    # Brand operations
    @staticmethod
    def get_brands(page=1, limit=50, filters=None):
        """Get brands with pagination"""
        try:
            query = Brand.query
            
            # Apply filters
            if filters:
                if filters.get('status'):
                    query = query.filter(Brand.status == filters['status'])
                if filters.get('validation_status'):
                    query = query.filter(Brand.validation_status == filters['validation_status'])
                if filters.get('search'):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            Brand.name.ilike(search_term),
                            Brand.email.ilike(search_term),
                            Brand.domain.ilike(search_term)
                        )
                    )
            
            total = query.count()
            brands = query.order_by(desc(Brand.created_at)).offset((page - 1) * limit).limit(limit).all()
            
            return {
                'data': [brand.to_dict() for brand in brands],
                'total': total,
                'page': page,
                'limit': limit,
                'pages': (total + limit - 1) // limit
            }
        except Exception as e:
            logger.error(f"Error getting brands: {str(e)}")
            return {'data': [], 'total': 0, 'page': page, 'limit': limit, 'pages': 0}
    
    @staticmethod
    def get_brand_by_id(brand_id):
        """Get brand by ID"""
        try:
            brand = Brand.query.get(brand_id)
            return brand.to_dict() if brand else None
        except Exception as e:
            logger.error(f"Error getting brand: {str(e)}")
            return None
    
    @staticmethod
    def get_brand_by_name(brand_name):
        """Get brand by name (case-insensitive)"""
        try:
            brand = Brand.query.filter(Brand.name.ilike(brand_name.strip())).first()
            return brand.to_dict() if brand else None
        except Exception as e:
            logger.error(f"Error getting brand by name: {str(e)}")
            return None
    
    @staticmethod
    def save_brand(brand_data, user_id=None):
        """Save brand to database"""
        try:
            brand = Brand(
                name=brand_data.get('name', ''),
                domain=brand_data.get('domain', ''),
                email=brand_data.get('email', ''),
                phone=brand_data.get('phone', ''),
                description=brand_data.get('description', ''),
                industry=brand_data.get('industry', ''),
                location=brand_data.get('location', ''),
                status=brand_data.get('status', 'active'),
                is_duplicate=brand_data.get('is_duplicate', False),
                validation_status=brand_data.get('validation_status', 'pending'),
                validation_issues=brand_data.get('validation_issues'),
                notes=brand_data.get('notes', ''),
                created_by=user_id
            )
            
            # Set social media
            if brand_data.get('social_media'):
                brand.set_social_media(brand_data['social_media'])
            
            db.session.add(brand)
            db.session.commit()
            
            logger.info(f"Brand saved: {brand.id}")
            return brand.to_dict()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving brand: {str(e)}")
            raise
    
    # QA Analysis operations
    @staticmethod
    def save_qa_analysis(brand_id, analysis_data, user_id=None):
        """Save QA analysis"""
        try:
            analysis = QAAnalysis(
                brand_id=brand_id,
                brand_name=analysis_data.get('brand_name', ''),
                profit_margin=analysis_data.get('profit_margin'),
                average_price=analysis_data.get('average_price'),
                min_price=analysis_data.get('min_price'),
                max_price=analysis_data.get('max_price'),
                product_count=analysis_data.get('product_count', 0),
                competition_score=analysis_data.get('competition_score'),
                status=analysis_data.get('status', 'unprofitable'),
                notes=analysis_data.get('notes', ''),
                analyzed_by=user_id
            )
            
            if analysis_data.get('analysis_data'):
                analysis.set_analysis_data(analysis_data['analysis_data'])
            
            db.session.add(analysis)
            db.session.commit()
            
            return analysis.to_dict()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving QA analysis: {str(e)}")
            raise
    
    @staticmethod
    def get_qa_metrics(brand_id):
        """Get QA metrics for a brand"""
        try:
            analyses = QAAnalysis.query.filter_by(brand_id=brand_id).order_by(desc(QAAnalysis.created_at)).all()
            if not analyses:
                return {}
            
            latest = analyses[0]
            return latest.to_dict()
        except Exception as e:
            logger.error(f"Error getting QA metrics: {str(e)}")
            return {}
    
    @staticmethod
    def get_qa_analyses(page=1, limit=50, filters=None):
        """Get QA analyses with pagination"""
        try:
            query = QAAnalysis.query
            
            # Apply filters
            if filters:
                if filters.get('status'):
                    query = query.filter(QAAnalysis.status == filters['status'])
                if filters.get('brand_id'):
                    query = query.filter(QAAnalysis.brand_id == filters['brand_id'])
            
            total = query.count()
            analyses = query.order_by(desc(QAAnalysis.created_at)).offset((page - 1) * limit).limit(limit).all()
            
            return {
                'data': [analysis.to_dict() for analysis in analyses],
                'total': total,
                'page': page,
                'limit': limit,
                'pages': (total + limit - 1) // limit
            }
        except Exception as e:
            logger.error(f"Error getting QA analyses: {str(e)}")
            return {'data': [], 'total': 0, 'page': page, 'limit': limit, 'pages': 0}

