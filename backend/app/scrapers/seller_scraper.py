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
    """Seller Scraper - 70% Automated Seller Sniping"""
    
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
    
    def extract_brands_from_storefront(self, seller_url, max_pages=10):
        """
        Bot scrapes target seller storefronts and extracts all brand names - 70% Automated
        Returns list of unique brand names found
        """
        try:
            if not self.driver:
                self._setup_driver()
            
            logger.info(f"🤖 Scraping seller storefront for brands: {seller_url}")
            brands_found = set()  # Use set to avoid duplicates
            
            # Navigate to seller storefront
            self.driver.get(seller_url)
            time.sleep(3)
            
            # Extract brands from current page
            page_brands = self._extract_brands_from_page()
            brands_found.update(page_brands)
            
            # Navigate through multiple pages if available
            for page_num in range(2, max_pages + 1):
                try:
                    # Try to find and click "Next" button
                    next_button = self.driver.find_elements(
                        By.CSS_SELECTOR, 
                        'a[aria-label="Next"], .pagnNext, [data-page="next"], .a-pagination .a-last a'
                    )
                    
                    if next_button and next_button[0].is_displayed():
                        next_button[0].click()
                        time.sleep(3)  # Wait for page load
                        
                        # Extract brands from this page
                        page_brands = self._extract_brands_from_page()
                        brands_found.update(page_brands)
                        logger.info(f"📦 Page {page_num}: Found {len(page_brands)} brands")
                    else:
                        logger.info(f"⏹️ No more pages. Stopped at page {page_num - 1}")
                        break
                except Exception as e:
                    logger.warning(f"Error navigating to page {page_num}: {str(e)}")
                    break
            
            brands_list = list(brands_found)
            logger.info(f"✅ Extracted {len(brands_list)} unique brands from seller storefront")
            return brands_list
            
        except Exception as e:
            logger.error(f"Error extracting brands from storefront: {str(e)}")
            return []
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
    
    def _extract_brands_from_page(self):
        """Extract brand names from current page"""
        try:
            brands = set()
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Method 1: Extract from product brand links/attributes
            # Amazon product pages have brand information in various places
            brand_selectors = [
                'a[href*="/s?k="]',  # Brand links
                '.a-text-bold',  # Bold text (often brand names)
                '[data-brand]',  # Data attribute
                '.a-size-base-plus',  # Product title area
                'span.a-text-bold',  # Brand spans
            ]
            
            for selector in brand_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()
                        # Filter out common non-brand text
                        if text and len(text) > 2 and len(text) < 50:
                            # Check if it looks like a brand name
                            if self._is_likely_brand_name(text):
                                brands.add(text)
                except:
                    continue
            
            # Method 2: Extract from product titles (brand is often first word/phrase)
            try:
                product_titles = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'h2 a.a-link-normal, .s-title-instructions-style h2 a, [data-cy="title-recipe"] a'
                )
                
                for title_element in product_titles:
                    title_text = title_element.text.strip()
                    # Extract brand from title (usually first 1-3 words)
                    if title_text:
                        words = title_text.split()
                        # Try first word, first two words, first three words
                        for word_count in [1, 2, 3]:
                            if len(words) >= word_count:
                                potential_brand = ' '.join(words[:word_count])
                                if self._is_likely_brand_name(potential_brand):
                                    brands.add(potential_brand)
            except:
                pass
            
            # Method 3: Extract from page source using regex
            try:
                page_text = self.driver.page_source
                # Look for brand patterns in HTML
                brand_patterns = [
                    r'data-brand="([^"]+)"',
                    r'brand[:\s]+([A-Z][a-zA-Z\s]+)',
                    r'"brandName":"([^"]+)"',
                ]
                
                for pattern in brand_patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    for match in matches:
                        if self._is_likely_brand_name(match):
                            brands.add(match.strip())
            except:
                pass
            
            return list(brands)
            
        except Exception as e:
            logger.error(f"Error extracting brands from page: {str(e)}")
            return []
    
    def _is_likely_brand_name(self, text):
        """Check if text is likely a brand name"""
        if not text or len(text) < 2:
            return False
        
        # Filter out common non-brand words
        non_brand_words = [
            'amazon', 'seller', 'store', 'shop', 'buy', 'now', 'price', 
            'shipping', 'free', 'prime', 'add', 'cart', 'wishlist',
            'review', 'rating', 'stars', 'customer', 'product', 'item',
            'see', 'more', 'details', 'description', 'specifications',
            'next', 'previous', 'page', 'results', 'showing'
        ]
        
        text_lower = text.lower().strip()
        
        # Check if it's a non-brand word
        if text_lower in non_brand_words:
            return False
        
        # Check if it's too long (likely not a brand)
        if len(text) > 50:
            return False
        
        # Check if it contains only numbers
        if text.replace(' ', '').isdigit():
            return False
        
        # Check if it's a URL or email
        if '@' in text or 'http' in text_lower or '.com' in text_lower:
            return False
        
        # Likely a brand if it starts with capital letter and has reasonable length
        if text[0].isupper() and 2 <= len(text) <= 40:
            return True
        
        return False

