from app.services.google_sheets_service import GoogleSheetsService
from app.utils.logger import get_logger
from datetime import datetime
import json

logger = get_logger(__name__)

class BackupService:
    """Service for automated data backups"""
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
    
    def backup_all_data(self):
        """Backup all data to backup sheet"""
        try:
            if not self.sheets_service.sheet:
                logger.warning("Google Sheets not configured for backup")
                return False
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Get all data
            sellers = self.sheets_service.get_sellers(page=1, limit=10000)
            brands = self.sheets_service.get_brands(page=1, limit=10000)
            
            # Create backup data structure
            backup_data = {
                'timestamp': timestamp,
                'sellers': sellers,
                'brands': brands,
                'backup_type': 'full'
            }
            
            # Save to backup sheet
            try:
                backup_sheet = self.sheets_service.sheet.worksheet('Backup')
            except:
                # Create backup sheet if it doesn't exist
                backup_sheet = self.sheets_service.sheet.add_worksheet(
                    title='Backup', rows=1000, cols=10
                )
            
            # Append backup record
            backup_sheet.append_row([
                timestamp,
                json.dumps(backup_data),
                len(sellers),
                len(brands)
            ])
            
            logger.info(f"Backup completed at {timestamp}")
            return True
            
        except Exception as e:
            logger.error(f"Error backing up data: {str(e)}")
            return False
    
    def create_backup_file(self, file_path=None):
        """Create a local backup file"""
        try:
            if not file_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_path = f"backup_{timestamp}.json"
            
            # Get all data
            sellers = self.sheets_service.get_sellers(page=1, limit=10000)
            brands = self.sheets_service.get_brands(page=1, limit=10000)
            
            backup_data = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'sellers': sellers,
                'brands': brands
            }
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Backup file created: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error creating backup file: {str(e)}")
            return None

