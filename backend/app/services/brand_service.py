from app.scrapers.brand_researcher import BrandResearcher
from app.services.database_service import DatabaseService
from app.services.data_validation_service import DataValidationService
from app.services.duplicate_detector_service import DuplicateDetectorService
from app.utils.logger import get_logger

logger = get_logger(__name__)

class BrandService:
    def __init__(self):
        self.researcher = BrandResearcher()
        self.db_service = DatabaseService()
        self.validator = DataValidationService()
        self.duplicate_detector = DuplicateDetectorService()
    
    def get_all_brands(self, page=1, limit=50, filters=None):
        """Get all brands from database"""
        try:
            result = self.db_service.get_brands(page=page, limit=limit, filters=filters)
            return result['data']
        except Exception as e:
            logger.error(f"Error fetching brands: {str(e)}")
            raise
    
    def get_brand_by_id(self, brand_id):
        """Get brand by ID"""
        try:
            brand = self.db_service.get_brand_by_id(brand_id)
            return brand
        except Exception as e:
            logger.error(f"Error fetching brand {brand_id}: {str(e)}")
            raise
    
    def research_brand(self, brand_name, user_id=None):
        """Research brand information"""
        try:
            logger.info(f"Researching brand: {brand_name}")
            
            # Research brand data
            brand_data = self.researcher.research(brand_name)
            
            # Validate data
            validated_data = self.validator.validate_brand_data(brand_data)
            
            # Check for duplicates before saving
            all_brands_result = self.db_service.get_brands(page=1, limit=1000)
            all_brands = all_brands_result.get('data', [])
            is_duplicate = self._check_duplicate(validated_data, all_brands)
            
            if is_duplicate:
                logger.warning(f"Duplicate brand detected: {validated_data.get('name')}")
                validated_data['is_duplicate'] = True
            
            # Save to database
            saved_brand = self.db_service.save_brand(validated_data, user_id)
            
            logger.info(f"Brand researched and saved: {saved_brand.get('id')}")
            return saved_brand
            
        except Exception as e:
            logger.error(f"Error researching brand: {str(e)}")
            raise
    
    def _check_duplicate(self, brand_data, existing_brands):
        """Check if brand is a duplicate"""
        try:
            name = brand_data.get('name', '').lower().strip()
            domain = brand_data.get('domain', '').lower().strip()
            
            for existing in existing_brands:
                existing_name = existing.get('name', '').lower().strip()
                existing_domain = existing.get('domain', '').lower().strip()
                
                # Check exact match
                if (name and existing_name and name == existing_name) or \
                   (domain and existing_domain and domain == existing_domain):
                    return True
            
            return False
        except:
            return False

