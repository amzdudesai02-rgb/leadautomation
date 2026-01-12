from app.utils.validators import validate_email, validate_url
from app.services.email_finder_service import EmailFinderService
from app.services.domain_validator_service import DomainValidatorService
from app.services.google_sheets_service import GoogleSheetsService
from app.utils.logger import get_logger
import re

logger = get_logger(__name__)

class DataValidationService:
    """Service for validating and cleaning data"""
    
    def __init__(self):
        self.email_finder = EmailFinderService()
        self.domain_validator = DomainValidatorService()
        self.sheets_service = GoogleSheetsService()
    
    def validate_seller_data(self, seller_data):
        """Validate seller data and clean it"""
        try:
            validated = seller_data.copy()
            issues = []
            
            # Validate name
            name = seller_data.get('name', '').strip()
            if not name or len(name) < 2:
                issues.append('Invalid name')
                validated['name'] = name if name else 'Unknown Seller'
            else:
                validated['name'] = self._clean_text(name)
            
            # Validate email
            email = seller_data.get('email', '').strip()
            if email:
                if not validate_email(email):
                    issues.append('Invalid email format')
                    validated['email'] = ''
                else:
                    validated['email'] = email.lower()
            else:
                validated['email'] = ''
            
            # Validate URL
            url = seller_data.get('store_url', '').strip()
            if url:
                if not validate_url(url):
                    issues.append('Invalid URL')
                    validated['store_url'] = ''
                else:
                    validated['store_url'] = self._normalize_url(url)
            else:
                validated['store_url'] = ''
            
            # Validate phone
            phone = seller_data.get('phone', '').strip()
            if phone:
                validated['phone'] = self._clean_phone(phone)
            else:
                validated['phone'] = ''
            
            validated['validation_status'] = 'valid' if not issues else 'invalid'
            validated['validation_issues'] = issues
            
            return validated
            
        except Exception as e:
            logger.error(f"Error validating seller data: {str(e)}")
            return seller_data
    
    def validate_brand_data(self, brand_data):
        """Validate brand data and clean it"""
        try:
            validated = brand_data.copy()
            issues = []
            
            # Validate name
            name = brand_data.get('name', '').strip()
            if not name or len(name) < 2:
                issues.append('Invalid brand name')
                validated['name'] = name if name else 'Unknown Brand'
            else:
                validated['name'] = self._clean_text(name)
            
            # Validate domain
            domain = brand_data.get('domain', '').strip()
            if domain:
                if not domain.startswith('http'):
                    domain = f"https://{domain}"
                
                domain_result = self.domain_validator.validate_domain(domain)
                if not domain_result['is_valid']:
                    issues.append('Invalid domain')
                    validated['domain'] = ''
                else:
                    validated['domain'] = domain_result.get('url', domain)
            else:
                validated['domain'] = ''
            
            # Validate email
            email = brand_data.get('email', '').strip()
            if email:
                if not validate_email(email):
                    issues.append('Invalid email format')
                    validated['email'] = ''
                else:
                    validated['email'] = email.lower()
            else:
                validated['email'] = ''
            
            # Validate social media
            social_media = brand_data.get('social_media', {})
            if isinstance(social_media, dict):
                validated['social_media'] = self._validate_social_media(social_media)
            else:
                validated['social_media'] = {}
            
            validated['validation_status'] = 'valid' if not issues else 'invalid'
            validated['validation_issues'] = issues
            
            return validated
            
        except Exception as e:
            logger.error(f"Error validating brand data: {str(e)}")
            return brand_data
    
    def clean_all_sellers(self):
        """Clean and validate all sellers in database"""
        try:
            sellers = self.sheets_service.get_sellers(page=1, limit=1000)
            cleaned = []
            
            for seller in sellers:
                cleaned_seller = self.validate_seller_data(seller)
                cleaned.append(cleaned_seller)
            
            logger.info(f"Cleaned {len(cleaned)} sellers")
            return cleaned
            
        except Exception as e:
            logger.error(f"Error cleaning sellers: {str(e)}")
            return []
    
    def clean_all_brands(self):
        """Clean and validate all brands in database"""
        try:
            brands = self.sheets_service.get_brands(page=1, limit=1000)
            cleaned = []
            
            for brand in brands:
                cleaned_brand = self.validate_brand_data(brand)
                cleaned.append(cleaned_brand)
            
            logger.info(f"Cleaned {len(cleaned)} brands")
            return cleaned
            
        except Exception as e:
            logger.error(f"Error cleaning brands: {str(e)}")
            return []
    
    def _clean_text(self, text):
        """Clean text data"""
        if not text:
            return ''
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove special characters (keep alphanumeric and common punctuation)
        text = re.sub(r'[^\w\s\-.,&()]', '', text)
        return text.strip()
    
    def _clean_phone(self, phone):
        """Clean and normalize phone number"""
        if not phone:
            return ''
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        # Format if it's a valid length
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        return phone
    
    def _normalize_url(self, url):
        """Normalize URL format"""
        if not url:
            return ''
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        return url
    
    def _validate_social_media(self, social_media):
        """Validate social media URLs"""
        validated = {}
        patterns = {
            'linkedin': r'linkedin\.com',
            'instagram': r'instagram\.com',
            'facebook': r'facebook\.com',
            'twitter': r'(twitter|x)\.com'
        }
        
        for platform, url in social_media.items():
            if url and isinstance(url, str):
                if validate_url(url) and re.search(patterns.get(platform, ''), url, re.IGNORECASE):
                    validated[platform] = url
        
        return validated

