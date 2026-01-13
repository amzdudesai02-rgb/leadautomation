"""
Brand Website Scraper - 80% Automated Brand Research
Scrapes brand websites for contact info, validates emails, finds social media
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import re
import time
from urllib.parse import urljoin, urlparse
from app.utils.logger import get_logger
from app.services.email_finder_service import EmailFinderService
from app.services.domain_validator_service import DomainValidatorService

logger = get_logger(__name__)

class BrandWebsiteScraper:
    """Scrapes brand websites for comprehensive contact information"""
    
    def __init__(self):
        self.driver = None
        self.email_finder = EmailFinderService()
        self.domain_validator = DomainValidatorService()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _setup_driver(self, headless=True):
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
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            logger.error(f"Error setting up Chrome driver: {str(e)}")
            return False
    
    def scrape_brand_website(self, domain_or_url, brand_name=None):
        """
        Comprehensive brand website scraping - 80% automated
        Returns pre-filled data with verification flags
        """
        try:
            # Normalize URL
            base_url = self._normalize_url(domain_or_url)
            if not base_url:
                return self._empty_result(brand_name, "Invalid domain")
            
            logger.info(f"Scraping brand website: {base_url}")
            
            # Initialize result structure
            result = {
                'brand_name': brand_name or self._extract_brand_name_from_domain(base_url),
                'domain': base_url,
                'website_url': base_url,
                'automation_percentage': 0,
                'needs_verification': True,
                'data': {
                    # Contact Information (80% automated)
                    'emails': {
                        'primary': '',
                        'contact': '',
                        'support': '',
                        'sales': '',
                        'all_found': [],
                        'verified': [],
                        'needs_verification': True
                    },
                    'phone': {
                        'primary': '',
                        'all_found': [],
                        'needs_verification': True
                    },
                    'address': {
                        'street': '',
                        'city': '',
                        'state': '',
                        'zip': '',
                        'country': '',
                        'full': '',
                        'needs_verification': True
                    },
                    # Social Media (80% automated)
                    'social_media': {
                        'linkedin': '',
                        'instagram': '',
                        'facebook': '',
                        'twitter': '',
                        'tiktok': '',
                        'youtube': '',
                        'pinterest': '',
                        'all_found': [],
                        'needs_verification': True
                    },
                    # Company Information (80% automated)
                    'company_info': {
                        'description': '',
                        'about': '',
                        'founded': '',
                        'employees': '',
                        'industry': '',
                        'needs_verification': True
                    },
                    # Key Personnel (needs human verification)
                    'key_personnel': {
                        'founder': '',
                        'ceo': '',
                        'contact_person': '',
                        'needs_verification': True
                    },
                    # Website Legitimacy (needs human check)
                    'legitimacy': {
                        'ssl_valid': False,
                        'domain_age': '',
                        'trust_score': 0,
                        'needs_human_check': True
                    }
                }
            }
            
            # Scrape using requests first (faster)
            try:
                response = self.session.get(base_url, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # Extract data from main page
                    self._extract_from_page(soup, base_url, result)
                    
                    # Scrape additional pages
                    self._scrape_contact_page(base_url, result)
                    self._scrape_about_page(base_url, result)
                    
            except Exception as e:
                logger.warning(f"Requests scraping failed, trying Selenium: {str(e)}")
                # Fallback to Selenium for JavaScript-heavy sites
                if self._setup_driver(headless=True):
                    try:
                        self.driver.get(base_url)
                        time.sleep(3)
                        html_content = self.driver.page_source
                        soup = BeautifulSoup(html_content, 'html.parser')
                        self._extract_from_page(soup, base_url, result)
                    finally:
                        if self.driver:
                            self.driver.quit()
                            self.driver = None
            
            # Validate and verify emails
            self._validate_emails(result)
            
            # Calculate automation percentage
            result['automation_percentage'] = self._calculate_automation_percentage(result)
            
            logger.info(f"Scraping completed. Automation: {result['automation_percentage']}%")
            return result
            
        except Exception as e:
            logger.error(f"Error scraping brand website: {str(e)}")
            return self._empty_result(brand_name, str(e))
    
    def _normalize_url(self, domain_or_url):
        """Normalize domain/URL to full URL"""
        try:
            if not domain_or_url:
                return None
            
            # Remove whitespace
            domain_or_url = domain_or_url.strip()
            
            # Add protocol if missing
            if not domain_or_url.startswith(('http://', 'https://')):
                # Try https first
                try:
                    test_url = f'https://{domain_or_url}'
                    response = requests.head(test_url, timeout=5, allow_redirects=True)
                    if response.status_code < 400:
                        return test_url
                except:
                    pass
                
                # Fallback to http
                return f'http://{domain_or_url}'
            
            return domain_or_url
        except:
            return None
    
    def _extract_from_page(self, soup, base_url, result):
        """Extract information from a page"""
        # Extract emails
        emails = self._extract_emails(soup, base_url, result)
        result['data']['emails']['all_found'].extend(emails)
        
        # Extract phone numbers
        phones = self._extract_phones(soup, result)
        result['data']['phone']['all_found'].extend(phones)
        
        # Extract addresses
        address = self._extract_address(soup)
        if address:
            result['data']['address'] = {**result['data']['address'], **address}
        
        # Extract social media links
        social_media = self._extract_social_media(soup, base_url)
        result['data']['social_media']['all_found'].extend(social_media)
        for platform, url in social_media.items():
            if url and not result['data']['social_media'].get(platform):
                result['data']['social_media'][platform] = url
        
        # Extract company info
        company_info = self._extract_company_info(soup)
        result['data']['company_info'].update(company_info)
        
        # Extract key personnel (limited - needs human verification)
        personnel = self._extract_key_personnel(soup)
        result['data']['key_personnel'].update(personnel)
    
    def _extract_emails(self, soup, base_url):
        """Extract email addresses from page"""
        emails = []
        
        # Find all email patterns in text
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        page_text = soup.get_text()
        found_emails = re.findall(email_pattern, page_text)
        
        # Also check mailto links
        mailto_links = soup.find_all('a', href=re.compile(r'^mailto:'))
        for link in mailto_links:
            email = link.get('href', '').replace('mailto:', '').split('?')[0]
            if email:
                found_emails.append(email)
        
        # Deduplicate and filter
        unique_emails = list(set([e.lower() for e in found_emails if '@' in e]))
        
        # Categorize emails
        for email in unique_emails:
            emails.append(email)
            
            # Categorize by common patterns
            email_lower = email.lower()
            if 'contact' in email_lower or 'info' in email_lower:
                if not result['data']['emails']['contact']:
                    result['data']['emails']['contact'] = email
            elif 'support' in email_lower or 'help' in email_lower:
                if not result['data']['emails']['support']:
                    result['data']['emails']['support'] = email
            elif 'sales' in email_lower:
                if not result['data']['emails']['sales']:
                    result['data']['emails']['sales'] = email
            elif not result['data']['emails']['primary']:
                result['data']['emails']['primary'] = email
        
        return emails
    
    def _extract_phones(self, soup, result=None):
        """Extract phone numbers from page"""
        phones = []
        
        # Common phone patterns
        phone_patterns = [
            r'\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
            r'\+?\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',  # International
        ]
        
        page_text = soup.get_text()
        for pattern in phone_patterns:
            found_phones = re.findall(pattern, page_text)
            phones.extend(found_phones)
        
        # Also check tel: links
        tel_links = soup.find_all('a', href=re.compile(r'^tel:'))
        for link in tel_links:
            phone = link.get('href', '').replace('tel:', '').strip()
            if phone:
                phones.append(phone)
        
        # Clean and deduplicate
        cleaned_phones = []
        for phone in phones:
            cleaned = re.sub(r'[^\d+]', '', phone)
            if len(cleaned) >= 10:  # Minimum valid phone length
                cleaned_phones.append(phone.strip())
        
        unique_phones = list(set(cleaned_phones))
        
        if result and unique_phones and not result['data']['phone']['primary']:
            result['data']['phone']['primary'] = unique_phones[0]
        
        return unique_phones
    
    def _extract_address(self, soup):
        """Extract physical address from page"""
        address = {}
        
        # Look for address in common locations
        address_selectors = [
            {'class': 'address'},
            {'class': 'contact-address'},
            {'id': 'address'},
            {'itemprop': 'address'},
        ]
        
        for selector in address_selectors:
            try:
                addr_elem = soup.find(**selector)
                if addr_elem:
                    addr_text = addr_elem.get_text().strip()
                    # Parse address components
                    parsed = self._parse_address(addr_text)
                    if parsed:
                        address.update(parsed)
                        address['full'] = addr_text
                        break
            except:
                continue
        
        return address
    
    def _parse_address(self, address_text):
        """Parse address text into components"""
        # Simple address parsing (can be enhanced)
        address = {}
        
        # Extract ZIP code
        zip_match = re.search(r'\b\d{5}(-\d{4})?\b', address_text)
        if zip_match:
            address['zip'] = zip_match.group(0)
        
        # Extract state (US states)
        us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
        
        for state in us_states:
            if state in address_text.upper():
                address['state'] = state
                break
        
        return address
    
    def _extract_social_media(self, soup, base_url):
        """Extract social media links"""
        social_media = {}
        
        # Find all links
        links = soup.find_all('a', href=True)
        
        social_patterns = {
            'linkedin': r'linkedin\.com/(?:company|in|pub)/[\w-]+',
            'instagram': r'instagram\.com/[\w.]+',
            'facebook': r'facebook\.com/[\w.]+',
            'twitter': r'(?:twitter|x)\.com/[\w]+',
            'tiktok': r'tiktok\.com/@?[\w]+',
            'youtube': r'youtube\.com/(?:channel|c|user|@)/[\w-]+',
            'pinterest': r'pinterest\.com/[\w]+',
        }
        
        for link in links:
            href = link.get('href', '')
            full_url = urljoin(base_url, href)
            
            for platform, pattern in social_patterns.items():
                if re.search(pattern, href, re.IGNORECASE):
                    if not social_media.get(platform):
                        if not href.startswith('http'):
                            social_media[platform] = f'https://{href}'
                        else:
                            social_media[platform] = full_url
                    break
        
        return social_media
    
    def _extract_company_info(self, soup):
        """Extract company information"""
        info = {}
        
        # Extract description/about
        desc_selectors = [
            {'class': 'description'},
            {'class': 'about'},
            {'id': 'about'},
            {'itemprop': 'description'},
        ]
        
        for selector in desc_selectors:
            try:
                desc_elem = soup.find(**selector)
                if desc_elem:
                    info['description'] = desc_elem.get_text().strip()[:500]  # Limit length
                    break
            except:
                continue
        
        # Extract founded year
        text = soup.get_text()
        founded_match = re.search(r'founded[:\s]+(\d{4})', text, re.IGNORECASE)
        if founded_match:
            info['founded'] = founded_match.group(1)
        
        # Extract industry
        industry_keywords = ['technology', 'retail', 'ecommerce', 'fashion', 'electronics', 
                           'food', 'health', 'beauty', 'home', 'sports', 'automotive']
        for keyword in industry_keywords:
            if keyword in text.lower():
                info['industry'] = keyword.capitalize()
                break
        
        return info
    
    def _extract_key_personnel(self, soup):
        """Extract key personnel (limited - needs human verification)"""
        personnel = {}
        
        # Look for founder/CEO mentions
        text = soup.get_text()
        
        # Simple pattern matching (can be enhanced)
        founder_match = re.search(r'founder[:\s]+([A-Z][a-z]+ [A-Z][a-z]+)', text, re.IGNORECASE)
        if founder_match:
            personnel['founder'] = founder_match.group(1)
        
        ceo_match = re.search(r'ceo[:\s]+([A-Z][a-z]+ [A-Z][a-z]+)', text, re.IGNORECASE)
        if ceo_match:
            personnel['ceo'] = ceo_match.group(1)
        
        return personnel
    
    def _scrape_contact_page(self, base_url, result):
        """Scrape contact page specifically"""
        contact_urls = [
            urljoin(base_url, '/contact'),
            urljoin(base_url, '/contact-us'),
            urljoin(base_url, '/contact.html'),
        ]
        
        for url in contact_urls:
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    self._extract_from_page(soup, base_url, result)
                    break
            except:
                continue
    
    def _scrape_about_page(self, base_url, result):
        """Scrape about page"""
        about_urls = [
            urljoin(base_url, '/about'),
            urljoin(base_url, '/about-us'),
            urljoin(base_url, '/about.html'),
        ]
        
        for url in about_urls:
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    self._extract_from_page(soup, base_url, result)
                    break
            except:
                continue
    
    def _validate_emails(self, result):
        """Validate email formats and verify with Hunter.io"""
        emails = result['data']['emails']['all_found']
        verified = []
        
        for email in emails:
            # Basic format validation
            if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email):
                # Verify with Hunter.io if available
                try:
                    verification = self.email_finder.verify_email(email)
                    if verification and verification.get('is_valid'):
                        verified.append(email)
                except:
                    # If verification fails, still include email but mark for verification
                    pass
        
        result['data']['emails']['verified'] = verified
        
        # Set primary email from verified list
        if verified and not result['data']['emails']['primary']:
            result['data']['emails']['primary'] = verified[0]
    
    def _calculate_automation_percentage(self, result):
        """Calculate how much data was automatically filled"""
        total_fields = 0
        filled_fields = 0
        
        # Emails
        if result['data']['emails']['primary']:
            filled_fields += 1
        total_fields += 1
        
        # Phone
        if result['data']['phone']['primary']:
            filled_fields += 1
        total_fields += 1
        
        # Social media (count each platform)
        social_count = sum(1 for k, v in result['data']['social_media'].items() 
                          if k != 'all_found' and k != 'needs_verification' and v)
        filled_fields += min(social_count, 5)  # Max 5 points for social media
        total_fields += 5
        
        # Company info
        if result['data']['company_info']['description']:
            filled_fields += 1
        total_fields += 1
        
        # Address
        if result['data']['address']['full']:
            filled_fields += 1
        total_fields += 1
        
        percentage = int((filled_fields / total_fields) * 100) if total_fields > 0 else 0
        return min(percentage, 80)  # Cap at 80% (20% always needs human verification)
    
    def _extract_brand_name_from_domain(self, url):
        """Extract brand name from domain"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            domain = domain.replace('www.', '').split('.')[0]
            return domain.replace('-', ' ').title()
        except:
            return 'Unknown Brand'
    
    def _empty_result(self, brand_name, error=None):
        """Return empty result structure"""
        return {
            'brand_name': brand_name or 'Unknown',
            'domain': '',
            'website_url': '',
            'automation_percentage': 0,
            'needs_verification': True,
            'error': error,
            'data': {
                'emails': {'primary': '', 'all_found': [], 'needs_verification': True},
                'phone': {'primary': '', 'all_found': [], 'needs_verification': True},
                'address': {'full': '', 'needs_verification': True},
                'social_media': {'needs_verification': True},
                'company_info': {'needs_verification': True},
                'key_personnel': {'needs_verification': True},
                'legitimacy': {'needs_human_check': True}
            }
        }

