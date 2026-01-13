"""
SmartScout Automation Scraper
Automates brand extraction from SmartScout platform
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import re
from app.utils.logger import get_logger
from app.config import Config

logger = get_logger(__name__)

class SmartScoutScraper:
    """SmartScout automation scraper for brand extraction"""
    
    def __init__(self):
        self.driver = None
        self.smartscout_url = "https://app.smartscout.com"  # Update with actual URL
        self.smartscout_username = Config.SMARTSCOUT_USERNAME if hasattr(Config, 'SMARTSCOUT_USERNAME') else None
        self.smartscout_password = Config.SMARTSCOUT_PASSWORD if hasattr(Config, 'SMARTSCOUT_PASSWORD') else None
    
    def _setup_driver(self, headless=False):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Chrome driver initialized")
            return True
        except Exception as e:
            logger.error(f"Error setting up Chrome driver: {str(e)}")
            raise
    
    def login(self):
        """Login to SmartScout"""
        try:
            if not self.driver:
                self._setup_driver()
            
            logger.info("Navigating to SmartScout...")
            self.driver.get(self.smartscout_url)
            time.sleep(3)
            
            # Wait for login form
            wait = WebDriverWait(self.driver, 10)
            
            # Find and fill username
            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            username_field.clear()
            username_field.send_keys(self.smartscout_username)
            
            # Find and fill password
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(self.smartscout_password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .login-button, [data-testid='login-button']")
            login_button.click()
            
            # Wait for dashboard
            time.sleep(5)
            logger.info("Login successful")
            return True
            
        except Exception as e:
            logger.error(f"Error logging into SmartScout: {str(e)}")
            return False
    
    def apply_filters(self, filters=None):
        """Apply filters to SmartScout search"""
        try:
            logger.info("Applying filters...")
            
            # Default filters
            default_filters = {
                'min_revenue': None,
                'max_revenue': None,
                'category': None,
                'country': 'US',
                'min_products': 1,
                'max_products': None,
                'brand_type': None
            }
            
            if filters:
                default_filters.update(filters)
            
            wait = WebDriverWait(self.driver, 10)
            
            # Navigate to brand search/filter page
            # Adjust selectors based on actual SmartScout interface
            try:
                # Look for filter button or filter panel
                filter_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".filter-button, [data-testid='filter-button'], .filters-toggle"))
                )
                filter_button.click()
                time.sleep(2)
            except:
                logger.warning("Filter button not found, trying direct navigation")
            
            # Apply revenue filters
            if default_filters.get('min_revenue'):
                try:
                    min_revenue = self.driver.find_element(By.NAME, "min_revenue")
                    min_revenue.clear()
                    min_revenue.send_keys(str(default_filters['min_revenue']))
                except:
                    logger.warning("Min revenue filter not found")
            
            if default_filters.get('max_revenue'):
                try:
                    max_revenue = self.driver.find_element(By.NAME, "max_revenue")
                    max_revenue.clear()
                    max_revenue.send_keys(str(default_filters['max_revenue']))
                except:
                    logger.warning("Max revenue filter not found")
            
            # Apply country filter
            if default_filters.get('country'):
                try:
                    country_select = Select(self.driver.find_element(By.NAME, "country"))
                    country_select.select_by_value(default_filters['country'])
                except:
                    logger.warning("Country filter not found")
            
            # Apply product count filter
            if default_filters.get('min_products'):
                try:
                    min_products = self.driver.find_element(By.NAME, "min_products")
                    min_products.clear()
                    min_products.send_keys(str(default_filters['min_products']))
                except:
                    logger.warning("Min products filter not found")
            
            # Click apply filters button
            try:
                apply_button = self.driver.find_element(By.CSS_SELECTOR, "button.apply-filters, [data-testid='apply-filters'], .apply-button")
                apply_button.click()
                time.sleep(3)
            except:
                logger.warning("Apply button not found, filters may auto-apply")
            
            logger.info("Filters applied successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error applying filters: {str(e)}")
            return False
    
    def extract_brands(self, count=100, scroll_delay=2):
        """Extract brands from SmartScout"""
        try:
            logger.info(f"Extracting {count} brands...")
            brands = []
            
            wait = WebDriverWait(self.driver, 10)
            
            # Wait for brand list to load
            time.sleep(3)
            
            # Scroll and extract brands
            extracted_count = 0
            scroll_attempts = 0
            max_scroll_attempts = 50  # Prevent infinite scrolling
            
            while extracted_count < count and scroll_attempts < max_scroll_attempts:
                # Get current page source
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # Find brand elements (adjust selectors based on actual SmartScout structure)
                brand_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    ".brand-item, .brand-card, [data-brand], .brand-row, tr[data-brand-id]"
                )
                
                # Extract brand data
                for element in brand_elements:
                    if extracted_count >= count:
                        break
                    
                    try:
                        brand_data = self._extract_brand_data(element)
                        if brand_data and brand_data.get('name'):
                            # Check if already extracted (avoid duplicates in same session)
                            if not any(b['name'] == brand_data['name'] for b in brands):
                                brands.append(brand_data)
                                extracted_count += 1
                                logger.info(f"Extracted brand {extracted_count}: {brand_data.get('name')}")
                    except Exception as e:
                        logger.warning(f"Error extracting brand data: {str(e)}")
                        continue
                
                # Scroll down to load more brands
                if extracted_count < count:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(scroll_delay)
                    scroll_attempts += 1
                    
                    # Check if new content loaded
                    new_brand_elements = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        ".brand-item, .brand-card, [data-brand], .brand-row, tr[data-brand-id]"
                    )
                    if len(new_brand_elements) == len(brand_elements):
                        # No new content, try clicking "Load More" if available
                        try:
                            load_more = self.driver.find_element(By.CSS_SELECTOR, ".load-more, [data-testid='load-more'], .next-page")
                            if load_more.is_displayed():
                                load_more.click()
                                time.sleep(3)
                        except:
                            logger.info("No more brands to load")
                            break
            
            logger.info(f"Extracted {len(brands)} brands")
            return brands
            
        except Exception as e:
            logger.error(f"Error extracting brands: {str(e)}")
            return brands  # Return whatever we got
    
    def _extract_brand_data(self, element):
        """Extract brand data from a single brand element"""
        try:
            brand_data = {
                'name': '',
                'domain': '',
                'revenue': '',
                'products_count': 0,
                'category': '',
                'country': '',
                'brand_url': '',
                'extracted_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Extract brand name (try multiple selectors)
            name_selectors = [
                ".brand-name, .name, [data-brand-name], h3, h4, .title, td:first-child"
            ]
            for selector in name_selectors:
                try:
                    name_elem = element.find_element(By.CSS_SELECTOR, selector)
                    brand_data['name'] = name_elem.text.strip()
                    break
                except:
                    continue
            
            # Extract domain
            try:
                domain_elem = element.find_element(By.CSS_SELECTOR, ".domain, .website, [data-domain], a[href*='http']")
                domain_url = domain_elem.get_attribute('href') or domain_elem.text.strip()
                brand_data['domain'] = self._clean_domain(domain_url)
            except:
                pass
            
            # Extract revenue
            try:
                revenue_elem = element.find_element(By.CSS_SELECTOR, ".revenue, [data-revenue], .sales")
                brand_data['revenue'] = revenue_elem.text.strip()
            except:
                pass
            
            # Extract product count
            try:
                products_elem = element.find_element(By.CSS_SELECTOR, ".products, .product-count, [data-products]")
                products_text = products_elem.text.strip()
                # Extract number from text
                numbers = re.findall(r'\d+', products_text)
                if numbers:
                    brand_data['products_count'] = int(numbers[0])
            except:
                pass
            
            # Extract category
            try:
                category_elem = element.find_element(By.CSS_SELECTOR, ".category, [data-category]")
                brand_data['category'] = category_elem.text.strip()
            except:
                pass
            
            # Extract country
            try:
                country_elem = element.find_element(By.CSS_SELECTOR, ".country, [data-country], .flag")
                brand_data['country'] = country_elem.text.strip() or country_elem.get_attribute('title')
            except:
                pass
            
            # Extract brand URL (link to brand page)
            try:
                link_elem = element.find_element(By.CSS_SELECTOR, "a")
                brand_data['brand_url'] = link_elem.get_attribute('href')
            except:
                pass
            
            return brand_data
            
        except Exception as e:
            logger.warning(f"Error extracting brand data from element: {str(e)}")
            return None
    
    def _clean_domain(self, url_or_domain):
        """Clean and normalize domain URL"""
        try:
            if not url_or_domain:
                return ''
            
            # Remove protocol
            domain = re.sub(r'^https?://', '', url_or_domain)
            # Remove www
            domain = re.sub(r'^www\.', '', domain)
            # Remove path
            domain = domain.split('/')[0]
            # Remove trailing slash
            domain = domain.rstrip('/')
            
            return domain
        except:
            return url_or_domain
    
    def run_automation(self, filters=None, brand_count=100):
        """Run complete automation: login, apply filters, extract brands"""
        try:
            logger.info("Starting SmartScout automation...")
            
            # Setup driver
            if not self._setup_driver(headless=False):  # Set to True for production
                return {'success': False, 'error': 'Failed to setup driver'}
            
            # Login
            if not self.login():
                return {'success': False, 'error': 'Failed to login'}
            
            # Apply filters
            if not self.apply_filters(filters):
                logger.warning("Failed to apply filters, continuing anyway...")
            
            # Extract brands
            brands = self.extract_brands(count=brand_count)
            
            logger.info(f"Automation completed. Extracted {len(brands)} brands")
            
            return {
                'success': True,
                'brands': brands,
                'count': len(brands)
            }
            
        except Exception as e:
            logger.error(f"Error in SmartScout automation: {str(e)}")
            return {'success': False, 'error': str(e)}
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None

