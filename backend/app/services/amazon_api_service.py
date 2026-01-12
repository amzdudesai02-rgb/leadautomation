import requests
import hmac
import hashlib
import base64
import time
from urllib.parse import quote
from app.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)

class AmazonAPIService:
    """Amazon Product Advertising API 5.0 Service"""
    
    def __init__(self):
        self.access_key = Config.AMAZON_API_KEY
        self.secret_key = Config.AMAZON_SECRET_KEY
        self.associate_tag = Config.AMAZON_ASSOCIATE_TAG
        self.endpoint = Config.AMAZON_ENDPOINT or 'webservices.amazon.com'
        self.region = Config.AMAZON_REGION or 'us-east-1'
        self.marketplace = Config.AMAZON_MARKETPLACE or 'www.amazon.com'
    
    def _generate_signature(self, method, uri, query_string, payload):
        """Generate AWS signature for API request"""
        try:
            algorithm = 'AWS4-HMAC-SHA256'
            service = 'ProductAdvertisingAPI'
            host = self.endpoint
            region = self.region
            
            # Create canonical request
            canonical_uri = uri
            canonical_querystring = query_string
            canonical_headers = f'host:{host}\nx-amz-date:{self._get_amz_date()}\n'
            signed_headers = 'host;x-amz-date'
            payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
            
            canonical_request = f'{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}'
            
            # Create string to sign
            credential_scope = f'{self._get_date_stamp()}/{region}/{service}/aws4_request'
            string_to_sign = f'{algorithm}\n{self._get_amz_date()}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()}'
            
            # Calculate signature
            k_date = self._sign(f'AWS4{self.secret_key}', self._get_date_stamp())
            k_region = self._sign(k_date, region)
            k_service = self._sign(k_region, service)
            k_signing = self._sign(k_service, 'aws4_request')
            signature = hmac.new(k_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
            
            # Create authorization header
            authorization_header = f'{algorithm} Credential={self.access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'
            
            return authorization_header
        except Exception as e:
            logger.error(f"Error generating signature: {str(e)}")
            raise
    
    def _sign(self, key, msg):
        """HMAC signing"""
        return hmac.new(key.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).digest()
    
    def _get_date_stamp(self):
        """Get date stamp for signature"""
        return time.strftime('%Y%m%d', time.gmtime())
    
    def _get_amz_date(self):
        """Get Amazon date format"""
        return time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    
    def search_products(self, keywords, search_index='All', item_count=10):
        """Search for products on Amazon"""
        try:
            if not self.access_key or not self.secret_key:
                logger.warning("Amazon API credentials not configured")
                return []
            
            uri = '/paapi5/searchitems'
            payload = {
                'PartnerTag': self.associate_tag,
                'PartnerType': 'Associates',
                'Keywords': keywords,
                'SearchIndex': search_index,
                'ItemCount': item_count,
                'Resources': [
                    'Images.Primary.Large',
                    'ItemInfo.Title',
                    'Offers.Listings.Price',
                    'Offers.Listings.Availability.Message',
                    'ItemInfo.ByLineInfo',
                    'ItemInfo.Classifications',
                    'ItemInfo.ContentInfo',
                    'ItemInfo.ExternalIds',
                    'ItemInfo.Features',
                    'ItemInfo.ManufactureInfo',
                    'ItemInfo.ProductInfo',
                    'ItemInfo.TechnicalInfo',
                    'Offers.Listings.Condition',
                    'Offers.Listings.DeliveryInfo',
                    'Offers.Listings.MerchantInfo',
                    'Offers.Listings.Promotions',
                    'Offers.Summaries.HighestPrice',
                    'Offers.Summaries.LowestPrice',
                    'Offers.Summaries.OfferCount'
                ]
            }
            
            payload_str = str(payload).replace("'", '"')
            query_string = ''
            
            # Generate signature
            authorization = self._generate_signature('POST', uri, query_string, payload_str)
            
            # Make request
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'X-Amz-Target': 'com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems',
                'X-Amz-Date': self._get_amz_date(),
                'Authorization': authorization
            }
            
            url = f'https://{self.endpoint}{uri}'
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_search_results(data)
            else:
                logger.error(f"Amazon API error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching Amazon products: {str(e)}")
            return []
    
    def get_product_prices(self, asins):
        """Get product prices for given ASINs"""
        try:
            if not self.access_key or not self.secret_key:
                logger.warning("Amazon API credentials not configured")
                return {}
            
            uri = '/paapi5/getitems'
            payload = {
                'PartnerTag': self.associate_tag,
                'PartnerType': 'Associates',
                'ItemIds': asins if isinstance(asins, list) else [asins],
                'Resources': [
                    'Offers.Listings.Price',
                    'Offers.Listings.Availability',
                    'ItemInfo.Title',
                    'ItemInfo.ByLineInfo'
                ]
            }
            
            payload_str = str(payload).replace("'", '"')
            query_string = ''
            
            authorization = self._generate_signature('POST', uri, query_string, payload_str)
            
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'X-Amz-Target': 'com.amazon.paapi5.v1.ProductAdvertisingAPIv1.GetItems',
                'X-Amz-Date': self._get_amz_date(),
                'Authorization': authorization
            }
            
            url = f'https://{self.endpoint}{uri}'
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_item_results(data)
            else:
                logger.error(f"Amazon API error: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            logger.error(f"Error getting product prices: {str(e)}")
            return {}
    
    def _parse_search_results(self, data):
        """Parse search results from Amazon API"""
        products = []
        try:
            if 'SearchResult' in data and 'Items' in data['SearchResult']:
                for item in data['SearchResult']['Items']:
                    product = {
                        'asin': item.get('ASIN', ''),
                        'title': item.get('ItemInfo', {}).get('Title', {}).get('DisplayValue', ''),
                        'price': self._extract_price(item),
                        'availability': self._extract_availability(item),
                        'brand': item.get('ItemInfo', {}).get('ByLineInfo', {}).get('Brand', {}).get('DisplayValue', ''),
                        'url': f"https://{self.marketplace}/dp/{item.get('ASIN', '')}"
                    }
                    products.append(product)
        except Exception as e:
            logger.error(f"Error parsing search results: {str(e)}")
        
        return products
    
    def _parse_item_results(self, data):
        """Parse item results from Amazon API"""
        products = {}
        try:
            if 'ItemsResult' in data and 'Items' in data['ItemsResult']:
                for item in data['ItemsResult']['Items']:
                    asin = item.get('ASIN', '')
                    products[asin] = {
                        'asin': asin,
                        'title': item.get('ItemInfo', {}).get('Title', {}).get('DisplayValue', ''),
                        'price': self._extract_price(item),
                        'availability': self._extract_availability(item),
                        'brand': item.get('ItemInfo', {}).get('ByLineInfo', {}).get('Brand', {}).get('DisplayValue', '')
                    }
        except Exception as e:
            logger.error(f"Error parsing item results: {str(e)}")
        
        return products
    
    def _extract_price(self, item):
        """Extract price from item data"""
        try:
            offers = item.get('Offers', {})
            listings = offers.get('Listings', [])
            if listings:
                price = listings[0].get('Price', {})
                amount = price.get('Amount', 0)
                currency = price.get('Currency', 'USD')
                return {
                    'amount': float(amount) if amount else 0,
                    'currency': currency,
                    'display': f"{currency} {amount}" if amount else 'N/A'
                }
        except:
            pass
        return {'amount': 0, 'currency': 'USD', 'display': 'N/A'}
    
    def _extract_availability(self, item):
        """Extract availability from item data"""
        try:
            offers = item.get('Offers', {})
            listings = offers.get('Listings', [])
            if listings:
                availability = listings[0].get('Availability', {})
                return availability.get('Message', 'Unknown')
        except:
            pass
        return 'Unknown'

