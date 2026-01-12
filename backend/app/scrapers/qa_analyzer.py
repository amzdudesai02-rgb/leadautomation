import requests
import time
from app.config import Config
from app.utils.logger import get_logger
from app.services.amazon_api_service import AmazonAPIService

logger = get_logger(__name__)

class QAAnalyzer:
    def __init__(self):
        self.amazon_api = AmazonAPIService()
    
    def analyze(self, brand_data):
        """Perform QA analysis on brand"""
        try:
            logger.info(f"Analyzing brand: {brand_data.get('name')}")
            
            # Get Amazon prices
            prices = self._get_amazon_prices(brand_data)
            
            # Calculate profit metrics
            profit_metrics = self._calculate_profit_metrics(prices)
            
            # Generate competition score
            competition_score = self._calculate_competition_score(brand_data)
            
            analysis = {
                'brand_id': brand_data.get('id'),
                'brand_name': brand_data.get('name', ''),
                'profit_margin': profit_metrics.get('margin', 0),
                'average_price': profit_metrics.get('average_price', 0),
                'min_price': profit_metrics.get('min_price', 0),
                'max_price': profit_metrics.get('max_price', 0),
                'product_count': profit_metrics.get('product_count', 0),
                'competition_score': competition_score,
                'status': 'profitable' if profit_metrics.get('margin', 0) > 15 else 'unprofitable',
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing brand: {str(e)}")
            raise
    
    def _get_amazon_prices(self, brand_data):
        """Get Amazon prices for brand products"""
        try:
            brand_name = brand_data.get('name', '')
            if not brand_name:
                return []
            
            # Search for products by brand name
            products = self.amazon_api.search_products(brand_name, search_index='All', item_count=20)
            
            # Filter products by brand if available
            if brand_name:
                filtered_products = [
                    p for p in products 
                    if brand_name.lower() in p.get('brand', '').lower() or 
                       brand_name.lower() in p.get('title', '').lower()
                ]
                return filtered_products if filtered_products else products
            
            return products
        except Exception as e:
            logger.error(f"Error getting Amazon prices: {str(e)}")
            return []
    
    def _calculate_profit_metrics(self, prices):
        """Calculate profit metrics"""
        try:
            if not prices:
                return {'margin': 0, 'average_price': 0, 'min_price': 0, 'max_price': 0}
            
            # Extract prices
            price_amounts = []
            for product in prices:
                price_info = product.get('price', {})
                if isinstance(price_info, dict):
                    amount = price_info.get('amount', 0)
                    if amount > 0:
                        price_amounts.append(amount)
                elif isinstance(price_info, (int, float)):
                    if price_info > 0:
                        price_amounts.append(price_info)
            
            if not price_amounts:
                return {'margin': 0, 'average_price': 0, 'min_price': 0, 'max_price': 0}
            
            # Calculate metrics
            average_price = sum(price_amounts) / len(price_amounts)
            min_price = min(price_amounts)
            max_price = max(price_amounts)
            
            # Estimate profit margin (assuming 30% average margin for Amazon products)
            # This is a simplified calculation - adjust based on your business model
            estimated_cost = average_price * 0.70  # Assume 70% cost, 30% margin
            margin = ((average_price - estimated_cost) / average_price) * 100 if average_price > 0 else 0
            
            return {
                'margin': round(margin, 2),
                'average_price': round(average_price, 2),
                'min_price': round(min_price, 2),
                'max_price': round(max_price, 2),
                'product_count': len(price_amounts)
            }
        except Exception as e:
            logger.error(f"Error calculating profit metrics: {str(e)}")
            return {'margin': 0, 'average_price': 0, 'min_price': 0, 'max_price': 0}
    
    def _calculate_competition_score(self, brand_data):
        """Calculate competition score (0-100)"""
        try:
            score = 50  # Base score
            
            # Factor 1: Domain validity (0-20 points)
            domain = brand_data.get('domain', '')
            if domain and domain.startswith('http'):
                score += 20
            
            # Factor 2: Social media presence (0-20 points)
            social_media = brand_data.get('social_media', {})
            if isinstance(social_media, dict):
                social_count = sum(1 for v in social_media.values() if v)
                score += min(social_count * 5, 20)
            
            # Factor 3: Email availability (0-10 points)
            email = brand_data.get('email', '')
            if email:
                score += 10
            
            # Factor 4: Brand name quality (0-10 points)
            brand_name = brand_data.get('name', '')
            if brand_name and len(brand_name) > 3:
                score += 10
            
            # Factor 5: Product availability (0-40 points)
            # This would be enhanced with actual product data
            # For now, we'll use a placeholder
            
            return min(score, 100)  # Cap at 100
        except Exception as e:
            logger.error(f"Error calculating competition score: {str(e)}")
            return 0

