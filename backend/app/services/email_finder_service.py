import requests
from app.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)

class EmailFinderService:
    """Email Finder Service using Hunter.io API"""
    
    def __init__(self):
        self.api_key = Config.HUNTER_API_KEY
        self.base_url = 'https://api.hunter.io/v2'
    
    def find_email(self, domain, first_name=None, last_name=None):
        """Find email address for a domain and name"""
        try:
            if not self.api_key:
                logger.warning("Hunter.io API key not configured")
                return None
            
            url = f'{self.base_url}/email-finder'
            params = {
                'domain': domain,
                'api_key': self.api_key
            }
            
            if first_name:
                params['first_name'] = first_name
            if last_name:
                params['last_name'] = last_name
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data') and data['data'].get('email'):
                    return {
                        'email': data['data']['email'],
                        'score': data['data'].get('score', 0),
                        'sources': data['data'].get('sources', []),
                        'first_name': data['data'].get('first_name', ''),
                        'last_name': data['data'].get('last_name', ''),
                        'position': data['data'].get('position', ''),
                        'company': data['data'].get('company', ''),
                        'confidence': data['data'].get('confidence', 0)
                    }
            else:
                logger.warning(f"Hunter.io API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error finding email: {str(e)}")
            return None
    
    def verify_email(self, email):
        """Verify if an email address is valid"""
        try:
            if not self.api_key:
                logger.warning("Hunter.io API key not configured")
                return None
            
            url = f'{self.base_url}/email-verifier'
            params = {
                'email': email,
                'api_key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    return {
                        'email': data['data'].get('email', ''),
                        'result': data['data'].get('result', ''),
                        'score': data['data'].get('score', 0),
                        'sources': data['data'].get('sources', []),
                        'is_valid': data['data'].get('result') == 'deliverable'
                    }
            else:
                logger.warning(f"Hunter.io API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error verifying email: {str(e)}")
            return None
    
    def domain_search(self, domain, limit=10):
        """Search for emails in a domain"""
        try:
            if not self.api_key:
                logger.warning("Hunter.io API key not configured")
                return []
            
            url = f'{self.base_url}/domain-search'
            params = {
                'domain': domain,
                'api_key': self.api_key,
                'limit': limit
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data') and data['data'].get('emails'):
                    emails = []
                    for email_data in data['data']['emails']:
                        emails.append({
                            'email': email_data.get('value', ''),
                            'first_name': email_data.get('first_name', ''),
                            'last_name': email_data.get('last_name', ''),
                            'position': email_data.get('position', ''),
                            'sources': email_data.get('sources', []),
                            'confidence': email_data.get('confidence', 0)
                        })
                    return emails
            else:
                logger.warning(f"Hunter.io API error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching domain: {str(e)}")
            return []

