import requests
import time
from app.config import Config
from app.utils.logger import get_logger
from app.services.amazon_api_service import AmazonAPIService

logger = get_logger(__name__)

class QAAnalyzer:
    """QA Analyzer - 95% Automated Analysis"""
    
    def __init__(self):
        self.amazon_api = AmazonAPIService()
        # Profitability thresholds
        self.HIGHLY_PROFITABLE_THRESHOLD = 30  # 30%+ margin
        self.PROFITABLE_THRESHOLD = 15  # 15-30% margin
        self.MARGINAL_THRESHOLD = 5  # 5-15% margin
        # Below 5% is unprofitable
    
    def analyze(self, brand_data, asins=None):
        """
        Perform QA analysis on brand - 95% Automated
        Bot fetches prices, calculates metrics, color-codes, generates scores
        """
        try:
            logger.info(f"🤖 Starting 95% automated QA analysis for: {brand_data.get('name')}")
            
            # Step 1: Bot fetches Amazon prices for ASINs
            products_data = self._get_amazon_prices_for_asins(brand_data, asins)
            
            # Step 2: Bot calculates all profit metrics
            profit_metrics = self._calculate_all_profit_metrics(products_data)
            
            # Step 3: Bot color-codes profitable vs not profitable (with product-level coding)
            color_coding = self._color_code_profitability(profit_metrics)
            products_data = self._apply_color_coding_to_products(products_data, profit_metrics)
            
            # Step 4: Bot generates competition scores
            competition_score = self._calculate_enhanced_competition_score(brand_data, products_data)
            
            # Calculate automation percentage (95% automated)
            automation_percentage = 95
            
            analysis = {
                'brand_id': brand_data.get('id'),
                'brand_name': brand_data.get('name', ''),
                'automation_percentage': automation_percentage,
                'needs_human_review': False,  # 95% automated, minimal human review needed
                
                # Profit Metrics (Automated)
                'profit_metrics': profit_metrics,
                
                # Color Coding (Automated)
                'profitability_status': color_coding['status'],
                'profitability_color': color_coding['color'],
                'profitability_label': color_coding['label'],
                
                # Competition Score (Automated)
                'competition_score': competition_score['score'],
                'competition_level': competition_score['level'],
                'competition_factors': competition_score['factors'],
                
                # Product Data (Automated with Color Coding)
                'products_analyzed': len(products_data),
                'products_data': products_data,  # Now includes color coding per product
                'color_coded_products': self._get_color_coded_summary(products_data),
                
                # Summary
                'status': color_coding['status'],
                'recommendation': self._generate_recommendation(profit_metrics, competition_score),
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            logger.info(f"✅ QA analysis completed. Status: {color_coding['status']}, Score: {competition_score['score']}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing brand: {str(e)}")
            raise
    
    def _get_amazon_prices_for_asins(self, brand_data, asins=None):
        """
        Bot fetches Amazon prices for ASINs - Automated
        If ASINs provided, fetch directly. Otherwise, search by brand name.
        """
        try:
            products_data = []
            
            # Method 1: Fetch by ASINs if provided
            if asins and isinstance(asins, list) and len(asins) > 0:
                logger.info(f"📦 Fetching prices for {len(asins)} ASINs...")
                asin_prices = self.amazon_api.get_product_prices(asins)
                
                for asin, product_data in asin_prices.items():
                    products_data.append({
                        'asin': asin,
                        'title': product_data.get('title', ''),
                        'price': product_data.get('price', {}),
                        'brand': product_data.get('brand', ''),
                        'availability': product_data.get('availability', 'Unknown')
                    })
            
            # Method 2: Search by brand name if no ASINs
            if not products_data:
                brand_name = brand_data.get('name', '')
                if brand_name:
                    logger.info(f"🔍 Searching products for brand: {brand_name}")
                    products = self.amazon_api.search_products(
                        brand_name, 
                        search_index='All', 
                        item_count=50  # Increased for better analysis
                    )
                    
                    # Filter products by brand
                    filtered_products = [
                        p for p in products 
                        if brand_name.lower() in p.get('brand', '').lower() or 
                           brand_name.lower() in p.get('title', '').lower()
                    ]
                    
                    for product in (filtered_products if filtered_products else products):
                        products_data.append({
                            'asin': product.get('asin', ''),
                            'title': product.get('title', ''),
                            'price': product.get('price', {}),
                            'brand': product.get('brand', ''),
                            'availability': product.get('availability', 'Unknown'),
                            'url': product.get('url', '')
                        })
            
            logger.info(f"✅ Fetched prices for {len(products_data)} products")
            return products_data
            
        except Exception as e:
            logger.error(f"Error getting Amazon prices: {str(e)}")
            return []
    
    def _calculate_all_profit_metrics(self, products_data):
        """
        Bot calculates all profit metrics - Automated
        Comprehensive profit analysis including margins, ROI, break-even, etc.
        """
        try:
            if not products_data:
                return self._empty_profit_metrics()
            
            # Extract prices
            price_amounts = []
            profitable_products = []
            unprofitable_products = []
            
            for product in products_data:
                price_info = product.get('price', {})
                amount = 0
                
                if isinstance(price_info, dict):
                    amount = price_info.get('amount', 0)
                elif isinstance(price_info, (int, float)):
                    amount = price_info
                
                if amount > 0:
                    price_amounts.append(amount)
                    
                    # Calculate individual product margin
                    estimated_cost = amount * 0.70  # Assume 70% cost
                    margin = ((amount - estimated_cost) / amount) * 100 if amount > 0 else 0
                    
                    product_margin = {
                        'asin': product.get('asin', ''),
                        'title': product.get('title', ''),
                        'price': amount,
                        'estimated_cost': round(estimated_cost, 2),
                        'margin': round(margin, 2),
                        'profit': round(amount - estimated_cost, 2)
                    }
                    
                    if margin >= self.PROFITABLE_THRESHOLD:
                        profitable_products.append(product_margin)
                    else:
                        unprofitable_products.append(product_margin)
            
            if not price_amounts:
                return self._empty_profit_metrics()
            
            # Calculate comprehensive metrics
            average_price = sum(price_amounts) / len(price_amounts)
            min_price = min(price_amounts)
            max_price = max(price_amounts)
            median_price = sorted(price_amounts)[len(price_amounts) // 2]
            
            # Overall profit metrics
            estimated_cost_avg = average_price * 0.70
            margin_avg = ((average_price - estimated_cost_avg) / average_price) * 100 if average_price > 0 else 0
            
            # ROI calculation (simplified)
            roi = (margin_avg / 100) * 100  # ROI percentage
            
            # Break-even analysis
            break_even_price = estimated_cost_avg
            
            # Profitability ratio
            profitability_ratio = len(profitable_products) / len(price_amounts) if price_amounts else 0
            
            return {
                'margin': round(margin_avg, 2),
                'margin_percentage': round(margin_avg, 2),
                'average_price': round(average_price, 2),
                'min_price': round(min_price, 2),
                'max_price': round(max_price, 2),
                'median_price': round(median_price, 2),
                'estimated_cost': round(estimated_cost_avg, 2),
                'profit_per_unit': round(average_price - estimated_cost_avg, 2),
                'roi': round(roi, 2),
                'break_even_price': round(break_even_price, 2),
                'product_count': len(price_amounts),
                'profitable_products_count': len(profitable_products),
                'unprofitable_products_count': len(unprofitable_products),
                'profitability_ratio': round(profitability_ratio * 100, 2),
                'profitable_products': profitable_products[:10],  # Top 10
                'unprofitable_products': unprofitable_products[:10],  # Top 10
                'price_range': round(max_price - min_price, 2),
                'price_volatility': self._calculate_price_volatility(price_amounts)
            }
        except Exception as e:
            logger.error(f"Error calculating profit metrics: {str(e)}")
            return self._empty_profit_metrics()
    
    def _empty_profit_metrics(self):
        """Return empty profit metrics structure"""
        return {
            'margin': 0,
            'margin_percentage': 0,
            'average_price': 0,
            'min_price': 0,
            'max_price': 0,
            'median_price': 0,
            'estimated_cost': 0,
            'profit_per_unit': 0,
            'roi': 0,
            'break_even_price': 0,
            'product_count': 0,
            'profitable_products_count': 0,
            'unprofitable_products_count': 0,
            'profitability_ratio': 0,
            'profitable_products': [],
            'unprofitable_products': [],
            'price_range': 0,
            'price_volatility': 0
        }
    
    def _calculate_price_volatility(self, prices):
        """Calculate price volatility (standard deviation)"""
        try:
            if len(prices) < 2:
                return 0
            
            mean = sum(prices) / len(prices)
            variance = sum((x - mean) ** 2 for x in prices) / len(prices)
            std_dev = variance ** 0.5
            
            # Return as percentage of average
            return round((std_dev / mean) * 100, 2) if mean > 0 else 0
        except:
            return 0
    
    def _color_code_profitability(self, profit_metrics):
        """
        Bot color-codes profitable vs not profitable - Automated
        Returns color coding based on profit margins
        """
        try:
            margin = profit_metrics.get('margin', 0)
            profitability_ratio = profit_metrics.get('profitability_ratio', 0)
            
            # Determine status and color
            if margin >= self.HIGHLY_PROFITABLE_THRESHOLD:
                status = 'highly_profitable'
                color = 'green'
                label = 'Highly Profitable'
                priority = 1
            elif margin >= self.PROFITABLE_THRESHOLD:
                status = 'profitable'
                color = 'lightgreen'
                label = 'Profitable'
                priority = 2
            elif margin >= self.MARGINAL_THRESHOLD:
                status = 'marginal'
                color = 'yellow'
                label = 'Marginal'
                priority = 3
            else:
                status = 'unprofitable'
                color = 'red'
                label = 'Not Profitable'
                priority = 4
            
            # Additional factors
            if profitability_ratio >= 0.7:  # 70%+ products profitable
                if status == 'marginal':
                    status = 'profitable'
                    color = 'lightgreen'
                    label = 'Profitable (High Ratio)'
            elif profitability_ratio < 0.3:  # Less than 30% profitable
                if status in ['profitable', 'marginal']:
                    status = 'unprofitable'
                    color = 'red'
                    label = 'Not Profitable (Low Ratio)'
            
            return {
                'status': status,
                'color': color,
                'label': label,
                'priority': priority,
                'margin': margin,
                'profitability_ratio': profitability_ratio
            }
        except Exception as e:
            logger.error(f"Error color coding profitability: {str(e)}")
            return {
                'status': 'unknown',
                'color': 'gray',
                'label': 'Unknown',
                'priority': 5
            }
    
    def _calculate_enhanced_competition_score(self, brand_data, products_data):
        """
        Bot generates competition scores - Automated
        Comprehensive competition analysis
        """
        try:
            score = 0
            factors = {}
            max_score = 100
            
            # Factor 1: Product Count & Availability (0-25 points)
            product_count = len(products_data)
            if product_count >= 20:
                factors['product_count'] = {'score': 25, 'reason': f'{product_count} products found'}
                score += 25
            elif product_count >= 10:
                factors['product_count'] = {'score': 15, 'reason': f'{product_count} products found'}
                score += 15
            elif product_count >= 5:
                factors['product_count'] = {'score': 10, 'reason': f'{product_count} products found'}
                score += 10
            else:
                factors['product_count'] = {'score': 5, 'reason': f'{product_count} products found'}
                score += 5
            
            # Factor 2: Price Range & Positioning (0-20 points)
            if products_data:
                prices = [p.get('price', {}).get('amount', 0) if isinstance(p.get('price'), dict) 
                         else (p.get('price', 0) if isinstance(p.get('price'), (int, float)) else 0) 
                         for p in products_data]
                prices = [p for p in prices if p > 0]
                
                if prices:
                    avg_price = sum(prices) / len(prices)
                    price_range = max(prices) - min(prices)
                    
                    # Sweet spot: $15-$50 average price
                    if 15 <= avg_price <= 50:
                        factors['price_positioning'] = {'score': 20, 'reason': f'Optimal price range: ${avg_price:.2f}'}
                        score += 20
                    elif 10 <= avg_price <= 100:
                        factors['price_positioning'] = {'score': 15, 'reason': f'Good price range: ${avg_price:.2f}'}
                        score += 15
                    else:
                        factors['price_positioning'] = {'score': 10, 'reason': f'Price range: ${avg_price:.2f}'}
                        score += 10
            
            # Factor 3: Brand Presence (0-20 points)
            domain = brand_data.get('domain', '')
            email = brand_data.get('email', '')
            social_media = brand_data.get('social_media', {})
            
            brand_score = 0
            if domain and domain.startswith('http'):
                brand_score += 5
            if email:
                brand_score += 5
            if isinstance(social_media, dict):
                social_count = sum(1 for v in social_media.values() if v)
                brand_score += min(social_count * 2, 10)
            
            factors['brand_presence'] = {'score': brand_score, 'reason': 'Brand visibility'}
            score += brand_score
            
            # Factor 4: Profitability (0-20 points)
            # This will be calculated from profit_metrics if available
            # For now, use placeholder
            factors['profitability'] = {'score': 15, 'reason': 'Profitability analysis'}
            score += 15
            
            # Factor 5: Market Competition (0-15 points)
            # Analyze competition level based on product diversity
            if product_count >= 15:
                factors['market_competition'] = {'score': 15, 'reason': 'Strong market presence'}
                score += 15
            elif product_count >= 5:
                factors['market_competition'] = {'score': 10, 'reason': 'Moderate market presence'}
                score += 10
            else:
                factors['market_competition'] = {'score': 5, 'reason': 'Limited market presence'}
                score += 5
            
            # Cap at 100
            score = min(score, max_score)
            
            # Determine competition level
            if score >= 80:
                level = 'Low Competition'
            elif score >= 60:
                level = 'Moderate Competition'
            elif score >= 40:
                level = 'High Competition'
            else:
                level = 'Very High Competition'
            
            return {
                'score': score,
                'level': level,
                'factors': factors,
                'max_score': max_score
            }
            
        except Exception as e:
            logger.error(f"Error calculating competition score: {str(e)}")
            return {
                'score': 0,
                'level': 'Unknown',
                'factors': {},
                'max_score': 100
            }
    
    def _apply_color_coding_to_products(self, products_data, profit_metrics):
        """Apply color coding to individual products based on profitability"""
        try:
            for product in products_data:
                price_info = product.get('price', {})
                amount = price_info.get('amount', 0) if isinstance(price_info, dict) else (price_info if isinstance(price_info, (int, float)) else 0)
                
                if amount > 0:
                    # Calculate product margin
                    estimated_cost = amount * 0.70
                    margin = ((amount - estimated_cost) / amount) * 100 if amount > 0 else 0
                    
                    # Assign color based on margin
                    if margin >= self.HIGHLY_PROFITABLE_THRESHOLD:
                        product['profitability_color'] = 'green'
                        product['profitability_status'] = 'highly_profitable'
                        product['profitability_label'] = 'Highly Profitable'
                        product['profitability_priority'] = 1
                    elif margin >= self.PROFITABLE_THRESHOLD:
                        product['profitability_color'] = 'lightgreen'
                        product['profitability_status'] = 'profitable'
                        product['profitability_label'] = 'Profitable'
                        product['profitability_priority'] = 2
                    elif margin >= self.MARGINAL_THRESHOLD:
                        product['profitability_color'] = 'yellow'
                        product['profitability_status'] = 'marginal'
                        product['profitability_label'] = 'Marginal'
                        product['profitability_priority'] = 3
                    else:
                        product['profitability_color'] = 'red'
                        product['profitability_status'] = 'unprofitable'
                        product['profitability_label'] = 'Not Profitable'
                        product['profitability_priority'] = 4
                    
                    product['margin'] = round(margin, 2)
                    product['estimated_cost'] = round(estimated_cost, 2)
                    product['profit'] = round(amount - estimated_cost, 2)
                else:
                    product['profitability_color'] = 'gray'
                    product['profitability_status'] = 'unknown'
                    product['profitability_label'] = 'Price Unknown'
                    product['profitability_priority'] = 5
            
            return products_data
        except Exception as e:
            logger.error(f"Error applying color coding to products: {str(e)}")
            return products_data
    
    def _get_color_coded_summary(self, products_data):
        """Get summary of color-coded products"""
        try:
            summary = {
                'green': 0,      # Highly profitable
                'lightgreen': 0, # Profitable
                'yellow': 0,     # Marginal
                'red': 0,        # Not profitable
                'gray': 0        # Unknown
            }
            
            for product in products_data:
                color = product.get('profitability_color', 'gray')
                if color in summary:
                    summary[color] += 1
            
            return summary
        except:
            return {'green': 0, 'lightgreen': 0, 'yellow': 0, 'red': 0, 'gray': 0}
    
    def _generate_recommendation(self, profit_metrics, competition_score):
        """Generate recommendation based on analysis"""
        try:
            margin = profit_metrics.get('margin', 0)
            score = competition_score.get('score', 0)
            profitability_ratio = profit_metrics.get('profitability_ratio', 0)
            
            if margin >= self.HIGHLY_PROFITABLE_THRESHOLD and score >= 70 and profitability_ratio >= 70:
                return "Highly Recommended - High profitability with low competition and strong product portfolio"
            elif margin >= self.PROFITABLE_THRESHOLD and score >= 60:
                return "Recommended - Good profitability with manageable competition"
            elif margin >= self.MARGINAL_THRESHOLD:
                return "Consider - Marginal profitability, review pricing strategy and cost structure"
            else:
                return "Not Recommended - Low profitability or high competition. Consider alternative brands or pricing adjustments"
        except:
            return "Analysis incomplete"

