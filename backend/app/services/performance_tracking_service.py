from app.services.google_sheets_service import GoogleSheetsService
from app.utils.logger import get_logger
from datetime import datetime, timedelta
from collections import defaultdict

logger = get_logger(__name__)

class PerformanceTrackingService:
    """Service for tracking performance metrics and generating dashboard data"""
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
    
    def get_dashboard_metrics(self):
        """Get metrics for dashboard"""
        try:
            all_sellers = self.sheets_service.get_sellers(page=1, limit=10000)
            all_brands = self.sheets_service.get_brands(page=1, limit=10000)
            
            metrics = {
                'total_sellers': len(all_sellers),
                'total_brands': len(all_brands),
                'today_sellers': self._count_today(all_sellers),
                'today_brands': self._count_today(all_brands),
                'week_sellers': self._count_this_week(all_sellers),
                'week_brands': self._count_this_week(all_brands),
                'month_sellers': self._count_this_month(all_sellers),
                'month_brands': self._count_this_month(all_brands),
                'growth_rate': self._calculate_growth_rate(all_sellers, all_brands),
                'top_sources': self._get_top_sources(all_sellers, all_brands),
                'completion_rate': self._calculate_completion_rate(all_sellers, all_brands)
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting dashboard metrics: {str(e)}")
            return {}
    
    def get_trend_data(self, days=30):
        """Get trend data for charts"""
        try:
            all_sellers = self.sheets_service.get_sellers(page=1, limit=10000)
            all_brands = self.sheets_service.get_brands(page=1, limit=10000)
            
            trends = []
            for i in range(days):
                date = (datetime.now() - timedelta(days=days-i-1)).strftime('%Y-%m-%d')
                sellers_count = len([s for s in all_sellers if s.get('created_at', '').startswith(date)])
                brands_count = len([b for b in all_brands if b.get('created_at', '').startswith(date)])
                
                trends.append({
                    'date': date,
                    'sellers': sellers_count,
                    'brands': brands_count,
                    'total': sellers_count + brands_count
                })
            
            return trends
            
        except Exception as e:
            logger.error(f"Error getting trend data: {str(e)}")
            return []
    
    def get_performance_summary(self):
        """Get performance summary"""
        try:
            metrics = self.get_dashboard_metrics()
            trends = self.get_trend_data(7)  # Last 7 days
            
            summary = {
                'metrics': metrics,
                'trends': trends,
                'status': 'healthy' if metrics.get('growth_rate', 0) > 0 else 'needs_attention',
                'recommendations': self._get_recommendations(metrics, trends)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting performance summary: {str(e)}")
            return {}
    
    def _count_today(self, items):
        """Count items created today"""
        today = datetime.now().strftime('%Y-%m-%d')
        return len([item for item in items if item.get('created_at', '').startswith(today)])
    
    def _count_this_week(self, items):
        """Count items created this week"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_start_str = week_start.strftime('%Y-%m-%d')
        return len([item for item in items if item.get('created_at', '')[:10] >= week_start_str])
    
    def _count_this_month(self, items):
        """Count items created this month"""
        month_start = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        return len([item for item in items if item.get('created_at', '')[:10] >= month_start])
    
    def _calculate_growth_rate(self, sellers, brands):
        """Calculate growth rate"""
        try:
            today_count = self._count_today(sellers) + self._count_today(brands)
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            yesterday_count = len([s for s in sellers if s.get('created_at', '').startswith(yesterday)]) + \
                            len([b for b in brands if b.get('created_at', '').startswith(yesterday)])
            
            if yesterday_count > 0:
                growth = ((today_count - yesterday_count) / yesterday_count) * 100
                return round(growth, 2)
            return 0
        except:
            return 0
    
    def _get_top_sources(self, sellers, brands):
        """Get top sources of leads"""
        sources = defaultdict(int)
        for seller in sellers:
            url = seller.get('store_url', '')
            if 'amazon' in url.lower():
                sources['Amazon'] += 1
        for brand in brands:
            domain = brand.get('domain', '')
            if domain:
                sources['Direct Research'] += 1
        
        return dict(sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5])
    
    def _calculate_completion_rate(self, sellers, brands):
        """Calculate data completion rate"""
        try:
            total = len(sellers) + len(brands)
            if total == 0:
                return 0
            
            complete = 0
            for seller in sellers:
                if seller.get('email') and seller.get('name'):
                    complete += 1
            for brand in brands:
                if brand.get('email') and brand.get('domain'):
                    complete += 1
            
            return round((complete / total) * 100, 2)
        except:
            return 0
    
    def _get_recommendations(self, metrics, trends):
        """Get recommendations based on performance"""
        recommendations = []
        
        if metrics.get('growth_rate', 0) < 0:
            recommendations.append("Growth rate is negative. Review lead generation strategies.")
        
        if metrics.get('completion_rate', 0) < 70:
            recommendations.append("Data completion rate is low. Focus on data quality.")
        
        if len(trends) > 0:
            recent_trend = trends[-1]
            if recent_trend.get('total', 0) == 0:
                recommendations.append("No new leads today. Check automation processes.")
        
        return recommendations if recommendations else ["All systems operating normally."]

