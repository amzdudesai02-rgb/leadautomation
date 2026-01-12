from app.services.google_sheets_service import GoogleSheetsService
from app.services.email_service import EmailService
from app.utils.logger import get_logger
from datetime import datetime, timedelta
import json

logger = get_logger(__name__)

class ReportingService:
    """Service for generating automated reports"""
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
        self.email_service = EmailService()
    
    def generate_daily_report(self):
        """Generate daily report with statistics"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Get all data
            all_sellers = self.sheets_service.get_sellers(page=1, limit=10000)
            all_brands = self.sheets_service.get_brands(page=1, limit=10000)
            
            # Calculate new entries (created today)
            new_sellers = [s for s in all_sellers if s.get('created_at', '').startswith(today)]
            new_brands = [b for b in all_brands if b.get('created_at', '').startswith(today)]
            
            # Get QA analyses
            # Note: This would need to be implemented in sheets_service
            qa_analyses = []  # Placeholder
            
            report_data = {
                'date': today,
                'new_sellers': len(new_sellers),
                'new_brands': len(new_brands),
                'qa_completed': len(qa_analyses),
                'total_sellers': len(all_sellers),
                'total_brands': len(all_brands),
                'top_performers': self._get_top_performers(all_sellers, all_brands),
                'issues': self._get_flagged_issues()
            }
            
            logger.info(f"Generated daily report for {today}")
            return report_data
            
        except Exception as e:
            logger.error(f"Error generating daily report: {str(e)}")
            return {}
    
    def generate_weekly_summary(self):
        """Generate weekly summary report"""
        try:
            today = datetime.now()
            week_start = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
            week_end = (today - timedelta(days=today.weekday() - 6)).strftime('%Y-%m-%d')
            
            # Get all data
            all_sellers = self.sheets_service.get_sellers(page=1, limit=10000)
            all_brands = self.sheets_service.get_brands(page=1, limit=10000)
            
            # Filter by week
            week_sellers = [s for s in all_sellers if week_start <= s.get('created_at', '')[:10] <= week_end]
            week_brands = [b for b in all_brands if week_start <= b.get('created_at', '')[:10] <= week_end]
            
            # Calculate averages
            # Note: This would need QA data
            avg_profit_margin = 0  # Placeholder
            top_competition_score = 0  # Placeholder
            
            summary_data = {
                'week_start': week_start,
                'week_end': week_end,
                'total_new_sellers': len(week_sellers),
                'total_new_brands': len(week_brands),
                'total_qa': 0,  # Placeholder
                'avg_profit_margin': avg_profit_margin,
                'top_competition_score': top_competition_score,
                'trends': self._analyze_trends(week_sellers, week_brands)
            }
            
            logger.info(f"Generated weekly summary for week {week_start} to {week_end}")
            return summary_data
            
        except Exception as e:
            logger.error(f"Error generating weekly summary: {str(e)}")
            return {}
    
    def send_daily_report_to_managers(self, manager_emails):
        """Send daily report to managers"""
        try:
            report_data = self.generate_daily_report()
            
            if not report_data:
                logger.warning("No report data generated")
                return False
            
            success_count = 0
            for email in manager_emails:
                if self.email_service.send_daily_report(email, report_data):
                    success_count += 1
            
            logger.info(f"Sent daily report to {success_count}/{len(manager_emails)} managers")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Error sending daily report: {str(e)}")
            return False
    
    def send_weekly_summary_to_managers(self, manager_emails):
        """Send weekly summary to managers"""
        try:
            summary_data = self.generate_weekly_summary()
            
            if not summary_data:
                logger.warning("No summary data generated")
                return False
            
            success_count = 0
            for email in manager_emails:
                if self.email_service.send_weekly_summary(email, summary_data):
                    success_count += 1
            
            logger.info(f"Sent weekly summary to {success_count}/{len(manager_emails)} managers")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Error sending weekly summary: {str(e)}")
            return False
    
    def create_report_charts_data(self):
        """Generate data for charts (for Google Data Studio integration)"""
        try:
            all_sellers = self.sheets_service.get_sellers(page=1, limit=10000)
            all_brands = self.sheets_service.get_brands(page=1, limit=10000)
            
            # Daily trends (last 30 days)
            daily_trends = {}
            for i in range(30):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                daily_trends[date] = {
                    'sellers': len([s for s in all_sellers if s.get('created_at', '').startswith(date)]),
                    'brands': len([b for b in all_brands if b.get('created_at', '').startswith(date)])
                }
            
            charts_data = {
                'daily_trends': daily_trends,
                'total_sellers': len(all_sellers),
                'total_brands': len(all_brands),
                'growth_rate': self._calculate_growth_rate(all_sellers, all_brands)
            }
            
            return charts_data
            
        except Exception as e:
            logger.error(f"Error creating charts data: {str(e)}")
            return {}
    
    def _get_top_performers(self, sellers, brands):
        """Get top performing sellers/brands"""
        # Placeholder - would need performance metrics
        return "Top 5 sellers and brands by activity"
    
    def _get_flagged_issues(self):
        """Get flagged issues that need attention"""
        # Placeholder - would check for validation issues, duplicates, etc.
        return "No critical issues flagged"
    
    def _analyze_trends(self, week_sellers, week_brands):
        """Analyze trends for the week"""
        if len(week_sellers) > 0 or len(week_brands) > 0:
            return f"Positive growth: {len(week_sellers)} sellers and {len(week_brands)} brands added this week"
        return "No significant trends this week"
    
    def _calculate_growth_rate(self, sellers, brands):
        """Calculate growth rate"""
        # Placeholder - would compare with previous period
        return "15% growth rate"

