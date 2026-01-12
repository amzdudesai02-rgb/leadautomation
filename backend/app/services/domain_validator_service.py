import requests
import socket
from urllib.parse import urlparse
from app.utils.logger import get_logger

logger = get_logger(__name__)

class DomainValidatorService:
    """Domain validation service using DNS and WHOIS"""
    
    def __init__(self):
        pass
    
    def validate_domain(self, domain):
        """Validate if a domain exists and is accessible"""
        try:
            # Remove protocol if present
            if '://' in domain:
                parsed = urlparse(domain)
                domain = parsed.netloc or parsed.path
            
            # Remove www. if present
            domain = domain.replace('www.', '').strip()
            
            # Check DNS resolution
            try:
                socket.gethostbyname(domain)
                dns_valid = True
            except socket.gaierror:
                dns_valid = False
            
            # Check if domain is accessible via HTTP
            http_accessible = False
            status_code = None
            try:
                for protocol in ['https', 'http']:
                    try:
                        url = f'{protocol}://{domain}'
                        response = requests.get(url, timeout=5, allow_redirects=True)
                        if response.status_code == 200:
                            http_accessible = True
                            status_code = response.status_code
                            break
                    except:
                        continue
            except:
                pass
            
            return {
                'domain': domain,
                'dns_valid': dns_valid,
                'http_accessible': http_accessible,
                'status_code': status_code,
                'url': f'https://{domain}' if http_accessible else None,
                'is_valid': dns_valid and http_accessible
            }
            
        except Exception as e:
            logger.error(f"Error validating domain: {str(e)}")
            return {
                'domain': domain,
                'dns_valid': False,
                'http_accessible': False,
                'is_valid': False
            }
    
    def find_domain_from_brand(self, brand_name):
        """Try to find domain from brand name"""
        try:
            # Common domain patterns
            domain_variations = [
                brand_name.lower().replace(' ', ''),
                brand_name.lower().replace(' ', '-'),
                brand_name.lower().replace(' ', ''),
            ]
            
            # Try common TLDs
            tlds = ['com', 'net', 'org', 'io', 'co']
            
            for domain_base in domain_variations:
                for tld in tlds:
                    domain = f"{domain_base}.{tld}"
                    result = self.validate_domain(domain)
                    if result['is_valid']:
                        return result['url']
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding domain: {str(e)}")
            return None

