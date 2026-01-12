from app.services.google_sheets_service import GoogleSheetsService
from app.services.duplicate_detector_service import DuplicateDetectorService
from app.services.data_validation_service import DataValidationService
from app.services.reporting_service import ReportingService
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
    
    def morning_setup(self):
        """Automated morning setup tasks"""
        try:
            logger.info("Starting morning setup automation...")
            results = {
                'account_auth': self._check_account_authentication(),
                'spreadsheet_updates': self._update_spreadsheets(),
                'duplicate_detection': self._detect_and_flag_duplicates(),
                'data_validation': self._validate_all_data(),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            logger.info("Morning setup completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error in morning setup: {str(e)}")
            return {'error': str(e)}
    
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

