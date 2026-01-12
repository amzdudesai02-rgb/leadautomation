from app.scrapers.seller_scraper import SellerScraper
from app.services.database_service import DatabaseService
from app.services.data_validation_service import DataValidationService
from app.services.duplicate_detector_service import DuplicateDetectorService
from app.utils.logger import get_logger

logger = get_logger(__name__)

class SellerService:
    def __init__(self):
        self.scraper = SellerScraper()
        self.db_service = DatabaseService()
        self.validator = DataValidationService()
        self.duplicate_detector = DuplicateDetectorService()
    
    def get_all_sellers(self, page=1, limit=50, filters=None):
        """Get all sellers from database"""
        try:
            result = self.db_service.get_sellers(page=page, limit=limit, filters=filters)
            return result['data']
        except Exception as e:
            logger.error(f"Error fetching sellers: {str(e)}")
            raise
    
    def get_seller_by_id(self, seller_id):
        """Get seller by ID"""
        try:
            seller = self.db_service.get_seller_by_id(seller_id)
            return seller
        except Exception as e:
            logger.error(f"Error fetching seller {seller_id}: {str(e)}")
            raise
    
    def scrape_seller(self, url, user_id=None):
        """Scrape seller information from Amazon"""
        try:
            logger.info(f"Scraping seller from URL: {url}")
            
            # Scrape seller data
            seller_data = self.scraper.scrape(url)
            
            # Validate data
            validated_data = self.validator.validate_seller_data(seller_data)
            
            # Check for duplicates before saving
            all_sellers_result = self.db_service.get_sellers(page=1, limit=1000)
            all_sellers = all_sellers_result.get('data', [])
            is_duplicate = self._check_duplicate(validated_data, all_sellers)
            
            if is_duplicate:
                logger.warning(f"Duplicate seller detected: {validated_data.get('name')}")
                validated_data['is_duplicate'] = True
            
            # Save to database
            saved_seller = self.db_service.save_seller(validated_data, user_id)
            
            logger.info(f"Seller scraped and saved successfully: {saved_seller.get('id')}")
            return saved_seller
            
        except Exception as e:
            logger.error(f"Error scraping seller: {str(e)}")
            raise
    
    def _check_duplicate(self, seller_data, existing_sellers):
        """Check if seller is a duplicate"""
        try:
            name = seller_data.get('name', '').lower().strip()
            email = seller_data.get('email', '').lower().strip()
            url = seller_data.get('store_url', '').lower().strip()
            
            for existing in existing_sellers:
                existing_name = existing.get('name', '').lower().strip()
                existing_email = existing.get('email', '').lower().strip()
                existing_url = existing.get('store_url', '').lower().strip()
                
                # Check exact match
                if (name and existing_name and name == existing_name) or \
                   (email and existing_email and email == existing_email) or \
                   (url and existing_url and url == existing_url):
                    return True
            
            return False
        except:
            return False
    
    def update_seller(self, seller_id, data):
        """Update seller information"""
        try:
            updated = self.db_service.update_seller(seller_id, data)
            return updated
        except Exception as e:
            logger.error(f"Error updating seller: {str(e)}")
            raise
    
    def delete_seller(self, seller_id):
        """Delete a seller"""
        try:
            return self.db_service.delete_seller(seller_id)
        except Exception as e:
            logger.error(f"Error deleting seller: {str(e)}")
            raise

