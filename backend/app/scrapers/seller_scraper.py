from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urlparse
from app.utils.logger import get_logger
from app.services.email_finder_service import EmailFinderService

logger = get_logger(__name__)

class SellerScraper:
    def __init__(self):
        self.driver = None
        self.email_finder = EmailFinderService()
    
    def _setup_driver(self):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            logger.error(f"Error setting up Chrome driver: {str(e)}")
            raise
    
    def scrape(self, url):
        """Scrape seller information from Amazon"""
        try:
            if not self.driver:
                self._setup_driver()
            
            logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            time.sleep(3)  # Wait for page load
            
            # Extract seller information
            seller_data = {
                'name': self._extract_seller_name(),
                'email': self._extract_email(),
                'store_url': url,
                'phone': self._extract_phone(),
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return seller_data
            
        except Exception as e:
            logger.error(f"Error scraping seller: {str(e)}")
            raise
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
    
    def _extract_seller_name(self):
        """Extract seller name from page"""
        try:
            # Adjust selectors based on actual Amazon page structure
            name_element = self.driver.find_element(By.CSS_SELECTOR, '.seller-name, [data-seller-name]')
            return name_element.text.strip()
        except:
            return 'Unknown Seller'
    
    def _extract_email(self):
        """Extract email from page or use email finder"""
        try:
            # First, try to extract email from page
            page_source = self.driver.page_source
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, page_source)
            
            if emails:
                # Return first valid email
                return emails[0]
            
            # If no email found, try to extract domain and use email finder
            current_url = self.driver.current_url
            parsed_url = urlparse(current_url)
            domain = parsed_url.netloc.replace('www.', '')
            
            # Try to find seller name for better email search
            seller_name = self._extract_seller_name()
            if seller_name and seller_name != 'Unknown Seller':
                # Try to extract first and last name
                name_parts = seller_name.split()
                first_name = name_parts[0] if name_parts else None
                last_name = name_parts[-1] if len(name_parts) > 1 else None
                
                # Use email finder service
                email_data = self.email_finder.find_email(domain, first_name, last_name)
                if email_data and email_data.get('email'):
                    return email_data['email']
            
            return ''
        except Exception as e:
            logger.error(f"Error extracting email: {str(e)}")
            return ''
    
    def _extract_phone(self):
        """Extract phone number"""
        try:
            # Extract phone from page
            return ''
        except:
            return ''

