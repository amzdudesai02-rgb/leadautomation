from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import re
import time
from app.utils.logger import get_logger
from app.services.domain_validator_service import DomainValidatorService
from app.services.email_finder_service import EmailFinderService
from app.scrapers.brand_website_scraper import BrandWebsiteScraper

logger = get_logger(__name__)

class BrandResearcher:
    def __init__(self):
        self.driver = None
        self.domain_validator = DomainValidatorService()
        self.email_finder = EmailFinderService()
        self.website_scraper = BrandWebsiteScraper()  # Enhanced scraper
    
    def research(self, brand_name, use_enhanced_scraper=True):
        """
        Research brand information - 80% Automated
        Uses enhanced website scraper for comprehensive data extraction
        """
        try:
            logger.info(f"Researching brand: {brand_name} (80% automated)")
            
            # Find domain first
            domain = self._find_domain(brand_name)
            
            # Use enhanced website scraper for comprehensive data
            if use_enhanced_scraper and domain:
                logger.info("Using enhanced website scraper...")
                scraped_data = self.website_scraper.scrape_brand_website(domain, brand_name)
                
                # Convert to standard format
                brand_data = {
                    'name': scraped_data.get('brand_name', brand_name),
                    'domain': scraped_data.get('domain', domain),
                    'website_url': scraped_data.get('website_url', domain),
                    'email': scraped_data['data']['emails']['primary'] or scraped_data['data']['emails']['contact'] or '',
                    'phone': scraped_data['data']['phone']['primary'] or '',
                    'address': scraped_data['data']['address']['full'] or '',
                    'social_media': {
                        'linkedin': scraped_data['data']['social_media'].get('linkedin', ''),
                        'instagram': scraped_data['data']['social_media'].get('instagram', ''),
                        'facebook': scraped_data['data']['social_media'].get('facebook', ''),
                        'twitter': scraped_data['data']['social_media'].get('twitter', ''),
                        'tiktok': scraped_data['data']['social_media'].get('tiktok', ''),
                        'youtube': scraped_data['data']['social_media'].get('youtube', ''),
                    },
                    'company_info': scraped_data['data']['company_info'],
                    'key_personnel': scraped_data['data']['key_personnel'],
                    'automation_percentage': scraped_data.get('automation_percentage', 0),
                    'needs_verification': scraped_data.get('needs_verification', True),
                    'all_emails_found': scraped_data['data']['emails']['all_found'],
                    'verified_emails': scraped_data['data']['emails']['verified'],
                    'all_phones_found': scraped_data['data']['phone']['all_found'],
                    'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                logger.info(f"Brand research completed. Automation: {brand_data['automation_percentage']}%")
                return brand_data
            
            # Fallback to basic research
            logger.info("Using basic research method...")
            brand_data = {
                'name': brand_name,
                'domain': domain,
                'social_media': self._find_social_media(brand_name),
                'email': self._find_email(brand_name),
                'automation_percentage': 50,  # Basic method is less automated
                'needs_verification': True,
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return brand_data
            
        except Exception as e:
            logger.error(f"Error researching brand: {str(e)}")
            raise
    
    def _find_domain(self, brand_name):
        """Find brand domain"""
        try:
            # Use domain validator to find valid domain
            domain_result = self.domain_validator.find_domain_from_brand(brand_name)
            if domain_result:
                return domain_result
            
            # Fallback to common pattern
            domain_base = brand_name.lower().replace(' ', '')
            validation = self.domain_validator.validate_domain(f"{domain_base}.com")
            if validation['is_valid']:
                return validation['url']
            
            return f"https://{domain_base}.com"
        except Exception as e:
            logger.error(f"Error finding domain: {str(e)}")
            return f"https://{brand_name.lower().replace(' ', '')}.com"
    
    def _find_social_media(self, brand_name):
        """Find social media accounts"""
        try:
            social_media = {
                'linkedin': '',
                'instagram': '',
                'facebook': '',
                'twitter': ''
            }
            
            # Get domain first
            domain = self._find_domain(brand_name)
            if not domain or domain.startswith('https://'):
                domain_clean = domain.replace('https://', '').replace('http://', '').split('/')[0]
            else:
                domain_clean = domain
            
            # Try to find social media by scraping domain
            if domain and domain.startswith('http'):
                try:
                    response = requests.get(domain, timeout=5, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    })
                    if response.status_code == 200:
                        html = response.text
                        
                        # Look for social media links
                        linkedin_pattern = r'linkedin\.com/(?:company|in)/[\w-]+'
                        instagram_pattern = r'instagram\.com/[\w.]+'
                        facebook_pattern = r'facebook\.com/[\w.]+'
                        twitter_pattern = r'(?:twitter|x)\.com/[\w]+'
                        
                        linkedin_match = re.search(linkedin_pattern, html, re.IGNORECASE)
                        instagram_match = re.search(instagram_pattern, html, re.IGNORECASE)
                        facebook_match = re.search(facebook_pattern, html, re.IGNORECASE)
                        twitter_match = re.search(twitter_pattern, html, re.IGNORECASE)
                        
                        if linkedin_match:
                            social_media['linkedin'] = f"https://{linkedin_match.group(0)}"
                        if instagram_match:
                            social_media['instagram'] = f"https://{instagram_match.group(0)}"
                        if facebook_match:
                            social_media['facebook'] = f"https://{facebook_match.group(0)}"
                        if twitter_match:
                            social_media['twitter'] = f"https://{twitter_match.group(0)}"
                except:
                    pass
            
            return social_media
        except Exception as e:
            logger.error(f"Error finding social media: {str(e)}")
            return {
                'linkedin': '',
                'instagram': '',
                'facebook': '',
                'twitter': ''
            }
    
    def _find_email(self, brand_name):
        """Find brand email"""
        try:
            # Get domain first
            domain = self._find_domain(brand_name)
            if domain and domain.startswith('http'):
                domain_clean = domain.replace('https://', '').replace('http://', '').split('/')[0]
            else:
                domain_clean = domain or brand_name.lower().replace(' ', '') + '.com'
            
            # Use email finder service
            email_data = self.email_finder.domain_search(domain_clean, limit=1)
            if email_data and len(email_data) > 0:
                return email_data[0].get('email', '')
            
            # Try generic emails
            generic_emails = ['info', 'contact', 'hello', 'support']
            for generic in generic_emails:
                email = f"{generic}@{domain_clean}"
                verification = self.email_finder.verify_email(email)
                if verification and verification.get('is_valid'):
                    return email
            
            return ''
        except Exception as e:
            logger.error(f"Error finding email: {str(e)}")
            return ''

