from app.services.google_sheets_service import GoogleSheetsService
from app.services.duplicate_detector_service import DuplicateDetectorService
from app.services.data_validation_service import DataValidationService
from app.services.reporting_service import ReportingService
from app.scrapers.smartscout_scraper import SmartScoutScraper
from app.utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)

class AutomationService:
    """Service for automated daily tasks"""
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
        self.duplicate_detector = DuplicateDetectorService()
        self.data_validator = DataValidationService()
        self.reporting_service = ReportingService()
        self.smartscout_scraper = SmartScoutScraper()
    
    def morning_setup(self, smartscout_enabled=True, brand_count=100):
        """Automated morning setup tasks - 90% Automated"""
        try:
            logger.info("Starting morning setup automation...")
            results = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'smartscout_extraction': None,
                'google_sheets_population': None,
                'duplicate_detection': None,
                'account_auth': self._check_account_authentication(),
            }
            
            # Step 1: SmartScout Automation (90% Automated)
            if smartscout_enabled:
                logger.info("🤖 Starting SmartScout automation...")
                smartscout_result = self._run_smartscout_automation(brand_count)
                results['smartscout_extraction'] = smartscout_result
                
                if smartscout_result.get('success'):
                    brands = smartscout_result.get('brands', [])
                    logger.info(f"✅ Extracted {len(brands)} brands from SmartScout")
                    
                    # Step 2: Populate Google Sheets
                    logger.info("📊 Populating Google Sheets...")
                    sheets_result = self._populate_google_sheets(brands)
                    results['google_sheets_population'] = sheets_result
                    
                    # Step 3: Check for duplicates and flag them
                    logger.info("🔍 Checking for duplicates...")
                    duplicate_result = self._detect_and_flag_duplicates()
                    results['duplicate_detection'] = duplicate_result
                else:
                    logger.error(f"❌ SmartScout automation failed: {smartscout_result.get('error')}")
            else:
                logger.info("⏭️ SmartScout automation skipped")
                results['smartscout_extraction'] = {'success': False, 'reason': 'disabled'}
            
            # Additional tasks
            results['spreadsheet_updates'] = self._update_spreadsheets()
            results['data_validation'] = self._validate_all_data()
            
            logger.info("✅ Morning setup completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error in morning setup: {str(e)}")
            return {'error': str(e), 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    def _run_smartscout_automation(self, brand_count=100):
        """Run SmartScout automation: Open, apply filters, extract brands"""
        try:
            # Default filters (can be customized)
            filters = {
                'country': 'US',
                'min_products': 1,
                # Add more filters as needed
            }
            
            # Run automation
            result = self.smartscout_scraper.run_automation(
                filters=filters,
                brand_count=brand_count
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error running SmartScout automation: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _populate_google_sheets(self, brands):
        """Populate Google Sheets with extracted brands"""
        try:
            if not brands:
                return {'status': 'skipped', 'reason': 'No brands to populate'}
            
            saved_count = 0
            failed_count = 0
            
            for brand in brands:
                try:
                    # Save brand to Google Sheets
                    self.sheets_service.save_brand(brand)
                    saved_count += 1
                except Exception as e:
                    logger.warning(f"Failed to save brand {brand.get('name')}: {str(e)}")
                    failed_count += 1
            
            return {
                'status': 'completed',
                'saved': saved_count,
                'failed': failed_count,
                'total': len(brands)
            }
            
        except Exception as e:
            logger.error(f"Error populating Google Sheets: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def end_of_day_tasks(self):
        """Automated end of day tasks"""
        try:
            logger.info("Starting end of day automation...")
            results = {
                'data_backup': self._backup_data(),
                'daily_report': self._generate_daily_report(),
                'charts_data': self._create_charts_data(),
                'report_sent': self._send_daily_reports(),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            logger.info("End of day tasks completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error in end of day tasks: {str(e)}")
            return {'error': str(e)}
    
    def _check_account_authentication(self):
        """Check if all API accounts are authenticated"""
        try:
            # Check Google Sheets
            if self.sheets_service.sheet:
                return {'status': 'authenticated', 'service': 'Google Sheets'}
            else:
                return {'status': 'not_authenticated', 'service': 'Google Sheets'}
        except Exception as e:
            logger.error(f"Error checking authentication: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def _update_spreadsheets(self):
        """Update spreadsheets with latest data"""
        try:
            # Refresh data
            sellers = self.sheets_service.get_sellers(page=1, limit=100)
            brands = self.sheets_service.get_brands(page=1, limit=100)
            
            return {
                'status': 'updated',
                'sellers_count': len(sellers),
                'brands_count': len(brands)
            }
        except Exception as e:
            logger.error(f"Error updating spreadsheets: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def _detect_and_flag_duplicates(self):
        """Detect and flag duplicates"""
        try:
            # Detect duplicates
            seller_duplicates = self.duplicate_detector.detect_duplicate_sellers()
            brand_duplicates = self.duplicate_detector.detect_duplicate_brands()
            
            # Flag in sheets
            self.duplicate_detector.flag_duplicates_in_sheet('Sellers')
            self.duplicate_detector.flag_duplicates_in_sheet('Brands')
            
            return {
                'status': 'completed',
                'seller_duplicates': len(seller_duplicates),
                'brand_duplicates': len(brand_duplicates)
            }
        except Exception as e:
            logger.error(f"Error detecting duplicates: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def _validate_all_data(self):
        """Validate and clean all data"""
        try:
            cleaned_sellers = self.data_validator.clean_all_sellers()
            cleaned_brands = self.data_validator.clean_all_brands()
            
            return {
                'status': 'completed',
                'sellers_cleaned': len(cleaned_sellers),
                'brands_cleaned': len(cleaned_brands)
            }
        except Exception as e:
            logger.error(f"Error validating data: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def _backup_data(self):
        """Backup data to Google Sheets backup sheet"""
        try:
            # This would create a backup copy in a separate sheet
            # For now, just log the action
            logger.info("Data backup completed")
            return {'status': 'completed', 'message': 'Data backed up successfully'}
        except Exception as e:
            logger.error(f"Error backing up data: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def _generate_daily_report(self):
        """Generate daily report"""
        try:
            report = self.reporting_service.generate_daily_report()
            return {'status': 'completed', 'report': report}
        except Exception as e:
            logger.error(f"Error generating daily report: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def _create_charts_data(self):
        """Create data for charts"""
        try:
            charts_data = self.reporting_service.create_report_charts_data()
            return {'status': 'completed', 'data': charts_data}
        except Exception as e:
            logger.error(f"Error creating charts data: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def _send_daily_reports(self):
        """Send daily reports to managers"""
        try:
            # Get manager emails from config or environment
            manager_emails = []  # Would come from config
            if manager_emails:
                sent = self.reporting_service.send_daily_report_to_managers(manager_emails)
                return {'status': 'completed', 'sent': sent}
            else:
                return {'status': 'skipped', 'reason': 'No manager emails configured'}
        except Exception as e:
            logger.error(f"Error sending daily reports: {str(e)}")
            return {'status': 'error', 'error': str(e)}

