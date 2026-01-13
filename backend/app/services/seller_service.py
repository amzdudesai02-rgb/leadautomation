from app.scrapers.seller_scraper import SellerScraper
from app.services.database_service import DatabaseService
from app.services.data_validation_service import DataValidationService
from app.services.duplicate_detector_service import DuplicateDetectorService
from app.services.research_queue_service import ResearchQueueService
from app.utils.logger import get_logger

logger = get_logger(__name__)

class SellerService:
    def __init__(self):
        self.scraper = SellerScraper()
        self.db_service = DatabaseService()
        self.validator = DataValidationService()
        self.duplicate_detector = DuplicateDetectorService()
        self.research_queue = ResearchQueueService()
    
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
    
    def snipe_seller(self, seller_url, user_id=None, auto_queue=True):
        """
        Seller Sniping - 70% Automated
        Bot scrapes storefront, extracts brands, cross-checks database, adds to research queue
        Human selects sellers to target and verifies brand quality
        """
        try:
            logger.info(f"🎯 Starting 70% automated seller sniping for: {seller_url}")
            
            # Step 1: Bot scrapes target seller storefronts
            logger.info("🤖 Step 1: Scraping seller storefront...")
            brands_found = self.scraper.extract_brands_from_storefront(seller_url)
            
            if not brands_found:
                return {
                    'success': False,
                    'message': 'No brands found on seller storefront',
                    'automation_percentage': 70,
                    'brands_found': 0,
                    'brands_queued': 0
                }
            
            logger.info(f"✅ Found {len(brands_found)} brands on storefront")
            
            # Step 2: Bot cross-checks with database
            logger.info("🤖 Step 2: Cross-checking with database...")
            new_brands, existing_brands = self._cross_check_brands(brands_found)
            
            logger.info(f"✅ Cross-check complete: {len(new_brands)} new, {len(existing_brands)} existing")
            
            # Step 3: Bot adds new brands to research queue (if auto_queue enabled)
            brands_queued = []
            if auto_queue and new_brands:
                logger.info(f"🤖 Step 3: Adding {len(new_brands)} brands to research queue...")
                queue_result = self.research_queue.add_batch_to_queue(
                    new_brands,
                    source='seller_sniping',
                    priority='normal'
                )
                brands_queued = queue_result.get('added', [])
                logger.info(f"✅ Added {len(brands_queued)} brands to research queue")
            
            # Calculate automation percentage
            automation_percentage = 70  # 70% automated
            
            result = {
                'success': True,
                'automation_percentage': automation_percentage,
                'seller_url': seller_url,
                'brands_found': len(brands_found),
                'brands_list': brands_found,
                'new_brands': new_brands,
                'existing_brands': existing_brands,
                'brands_queued': brands_queued if auto_queue else [],
                'needs_human_review': True,  # Human needs to verify brand quality
                'human_tasks': [
                    'Review extracted brands for quality',
                    'Select which brands to research',
                    'Verify brand names are correct',
                    'Approve brands for research queue'
                ],
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            logger.info(f"✅ Seller sniping completed. Found {len(brands_found)} brands, {len(new_brands)} new")
            return result
            
        except Exception as e:
            logger.error(f"Error in seller sniping: {str(e)}")
            raise
    
    def _cross_check_brands(self, brand_names):
        """Cross-check brands with database to find new vs existing"""
        try:
            new_brands = []
            existing_brands = []
            
            # Get all existing brands from database
            all_brands_result = self.db_service.get_brands(page=1, limit=10000)
            existing_brand_names = set()
            
            if all_brands_result and all_brands_result.get('data'):
                for brand in all_brands_result['data']:
                    brand_name = brand.get('name', '').lower().strip()
                    if brand_name:
                        existing_brand_names.add(brand_name)
            
            # Check each found brand
            for brand_name in brand_names:
                brand_lower = brand_name.lower().strip()
                
                # Check for exact match
                if brand_lower in existing_brand_names:
                    existing_brands.append(brand_name)
                else:
                    # Check for similar matches (fuzzy)
                    is_similar = False
                    for existing_name in existing_brand_names:
                        # Simple similarity check (can be enhanced)
                        if brand_lower in existing_name or existing_name in brand_lower:
                            is_similar = True
                            existing_brands.append(brand_name)
                            break
                    
                    if not is_similar:
                        new_brands.append(brand_name)
            
            return new_brands, existing_brands
            
        except Exception as e:
            logger.error(f"Error cross-checking brands: {str(e)}")
            # If error, assume all are new
            return brand_names, []

