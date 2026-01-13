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
    
    def research_brand(self, brand_name, user_id=None, use_enhanced_scraper=True):
        """
        Research brand information - 80% Automated Hybrid Approach
        Bot pre-fills 80% of information, human verifies quality and fills missing 20%
        """
        try:
            logger.info(f"Researching brand: {brand_name} (80% automated)")
            
            # Research brand data using enhanced scraper
            brand_data = self.researcher.research(brand_name, use_enhanced_scraper=use_enhanced_scraper)
            
            # Validate data
            validated_data = self.validator.validate_brand_data(brand_data)
            
            # Mark fields that need human verification
            validated_data['verification_status'] = {
                'automation_percentage': brand_data.get('automation_percentage', 0),
                'needs_quality_check': True,
                'needs_missing_data_fill': brand_data.get('automation_percentage', 0) < 100,
                'needs_legitimacy_check': True,
                'fields_to_verify': self._get_fields_to_verify(brand_data)
            }
            
            # Check for duplicates before saving
            all_brands_result = self.db_service.get_brands(page=1, limit=1000)
            all_brands = all_brands_result.get('data', [])
            is_duplicate = self._check_duplicate(validated_data, all_brands)
            
            if is_duplicate:
                logger.warning(f"Duplicate brand detected: {validated_data.get('name')}")
                validated_data['is_duplicate'] = True
            
            # Save to database
            saved_brand = self.db_service.save_brand(validated_data, user_id)
            
            logger.info(f"Brand researched and saved: {saved_brand.get('id')}. Automation: {brand_data.get('automation_percentage', 0)}%")
            return saved_brand
            
        except Exception as e:
            logger.error(f"Error researching brand: {str(e)}")
            raise
    
    def _get_fields_to_verify(self, brand_data):
        """Get list of fields that need human verification"""
        fields_to_verify = []
        
        # Check which fields are missing or need verification
        if not brand_data.get('email'):
            fields_to_verify.append('email')
        if not brand_data.get('phone'):
            fields_to_verify.append('phone')
        if not brand_data.get('address'):
            fields_to_verify.append('address')
        
        # Social media - check if any are missing
        social_media = brand_data.get('social_media', {})
        if not any(social_media.values()):
            fields_to_verify.append('social_media')
        
        # Company info
        company_info = brand_data.get('company_info', {})
        if not company_info.get('description'):
            fields_to_verify.append('company_description')
        
        # Key personnel always needs verification
        fields_to_verify.append('key_personnel')
        
        # Website legitimacy always needs human check
        fields_to_verify.append('website_legitimacy')
        
        return fields_to_verify
    
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

