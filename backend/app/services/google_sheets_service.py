import gspread
from google.oauth2.service_account import Credentials
from app.config import Config
from app.utils.logger import get_logger
import time

logger = get_logger(__name__)

class GoogleSheetsService:
    def __init__(self):
        self.sheet_id = Config.GOOGLE_SHEETS_SHEET_ID
        self.client = None
        self.sheet = None
        if self.sheet_id:
            try:
                self.client = self._get_client()
                self.sheet = self.client.open_by_key(self.sheet_id)
            except Exception as e:
                logger.warning(f"Google Sheets not configured: {str(e)}")
    
    def _get_client(self):
        """Initialize Google Sheets client"""
        try:
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            
            if Config.GOOGLE_SHEETS_CREDENTIALS:
                creds = Credentials.from_service_account_file(
                    Config.GOOGLE_SHEETS_CREDENTIALS, scopes=scope
                )
            else:
                # Fallback - return None if not configured
                logger.warning("Google Sheets credentials not configured")
                return None
            
            return gspread.authorize(creds)
        except Exception as e:
            logger.error(f"Error initializing Google Sheets client: {str(e)}")
            return None
    
    def get_sellers(self, page=1, limit=50):
        """Get sellers from Google Sheets"""
        if not self.sheet:
            return []
        try:
            worksheet = self.sheet.worksheet('Sellers')
            records = worksheet.get_all_records()
            
            # Pagination
            start = (page - 1) * limit
            end = start + limit
            return records[start:end]
        except Exception as e:
            logger.error(f"Error fetching sellers: {str(e)}")
            return []
    
    def save_seller(self, seller_data):
        """Save seller to Google Sheets"""
        if not self.sheet:
            return seller_data
        try:
            worksheet = self.sheet.worksheet('Sellers')
            worksheet.append_row([
                seller_data.get('name', ''),
                seller_data.get('email', ''),
                seller_data.get('store_url', ''),
                seller_data.get('phone', ''),
                seller_data.get('created_at', time.strftime('%Y-%m-%d %H:%M:%S'))
            ])
            return seller_data
        except Exception as e:
            logger.error(f"Error saving seller: {str(e)}")
            return seller_data
    
    def get_seller_by_id(self, seller_id):
        """Get seller by ID"""
        sellers = self.get_sellers()
        return next((s for s in sellers if str(s.get('id')) == str(seller_id)), None)
    
    def update_seller(self, seller_id, data):
        """Update seller"""
        # Implementation for updating seller
        return data
    
    def delete_seller(self, seller_id):
        """Delete seller"""
        # Implementation for deleting seller
        pass
    
    def get_brands(self, page=1, limit=50):
        """Get brands from Google Sheets"""
        if not self.sheet:
            return []
        try:
            worksheet = self.sheet.worksheet('Brands')
            records = worksheet.get_all_records()
            
            start = (page - 1) * limit
            end = start + limit
            return records[start:end]
        except Exception as e:
            logger.error(f"Error fetching brands: {str(e)}")
            return []
    
    def save_brand(self, brand_data):
        """Save brand to Google Sheets"""
        if not self.sheet:
            return brand_data
        try:
            worksheet = self.sheet.worksheet('Brands')
            worksheet.append_row([
                brand_data.get('name', ''),
                brand_data.get('domain', ''),
                str(brand_data.get('social_media', '')),
                brand_data.get('email', ''),
                brand_data.get('created_at', time.strftime('%Y-%m-%d %H:%M:%S'))
            ])
            return brand_data
        except Exception as e:
            logger.error(f"Error saving brand: {str(e)}")
            return brand_data
    
    def get_brand_by_id(self, brand_id):
        """Get brand by ID"""
        brands = self.get_brands()
        return next((b for b in brands if str(b.get('id')) == str(brand_id)), None)
    
    def save_qa_analysis(self, brand_id, analysis):
        """Save QA analysis results"""
        if not self.sheet:
            return analysis
        try:
            worksheet = self.sheet.worksheet('QA_Analysis')
            worksheet.append_row([
                brand_id,
                analysis.get('profit_margin', ''),
                analysis.get('competition_score', ''),
                analysis.get('status', ''),
                analysis.get('created_at', time.strftime('%Y-%m-%d %H:%M:%S'))
            ])
            return analysis
        except Exception as e:
            logger.error(f"Error saving QA analysis: {str(e)}")
            return analysis
    
    def get_qa_metrics(self, brand_id):
        """Get QA metrics"""
        # Implementation for getting QA metrics
        return {}

