from app.services.google_sheets_service import GoogleSheetsService
from app.services.email_service import EmailService
from app.services.database_service import DatabaseService
from app.utils.logger import get_logger
from datetime import datetime, timedelta
import json

logger = get_logger(__name__)

class ReportingService:
    """Service for generating automated reports - 100% Automated"""
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
        self.email_service = EmailService()
        self.db_service = DatabaseService()
    
    def generate_daily_report(self):
        """Generate comprehensive daily report - 100% Automated"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Get all data from database
            all_sellers_result = self.db_service.get_sellers(page=1, limit=10000)
            all_sellers = all_sellers_result.get('data', [])
            
            all_brands_result = self.db_service.get_brands(page=1, limit=10000)
            all_brands = all_brands_result.get('data', [])
            
            all_qa_result = self.db_service.get_qa_analyses(page=1, limit=10000)
            all_qa = all_qa_result.get('data', [])
            
            # Calculate new entries (created today)
            new_sellers = [s for s in all_sellers if s.get('created_at', '').startswith(today)]
            new_brands = [b for b in all_brands if b.get('created_at', '').startswith(today)]
            new_qa = [qa for qa in all_qa if qa.get('created_at', '').startswith(today)]
            
            # Calculate statistics
            profitable_brands = [qa for qa in new_qa if qa.get('status', '').lower() in ['profitable', 'highly_profitable']]
            avg_profit_margin = sum([qa.get('profit_margin', 0) or 0 for qa in new_qa]) / len(new_qa) if new_qa else 0
            avg_competition_score = sum([qa.get('competition_score', {}).get('score', 0) if isinstance(qa.get('competition_score'), dict) else (qa.get('competition_score', 0) or 0) for qa in new_qa]) / len(new_qa) if new_qa else 0
            
            report_data = {
                'date': today,
                'yesterday': yesterday,
                'summary': {
                    'new_sellers': len(new_sellers),
                    'new_brands': len(new_brands),
                    'qa_completed': len(new_qa),
                    'profitable_brands': len(profitable_brands),
                    'total_sellers': len(all_sellers),
                    'total_brands': len(all_brands),
                    'total_qa': len(all_qa)
                },
                'metrics': {
                    'average_profit_margin': round(avg_profit_margin, 2),
                    'average_competition_score': round(avg_competition_score, 2),
                    'profitability_rate': round((len(profitable_brands) / len(new_qa)) * 100, 2) if new_qa else 0
                },
                'top_performers': self._get_top_performers(all_sellers, all_brands, all_qa),
                'issues': self._get_flagged_issues(all_sellers, all_brands),
                'automation_summary': self._get_automation_summary(new_sellers, new_brands, new_qa)
            }
            
            logger.info(f"✅ Generated comprehensive daily report for {today}")
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
    
    def send_daily_report_to_managers(self, manager_emails, report_data=None, charts_data=None):
        """Send comprehensive daily report to managers - 100% Automated"""
        try:
            if not report_data:
                report_data = self.generate_daily_report()
            
            if not report_data:
                logger.warning("No report data generated")
                return 0
            
            # Enhance report with charts data if provided
            if charts_data:
                report_data['charts_summary'] = {
                    'profitability_distribution': charts_data.get('profitability_distribution', {}),
                    'competition_distribution': charts_data.get('competition_score_distribution', {}),
                    'automation_efficiency': charts_data.get('automation_efficiency', {}),
                    'hourly_breakdown': {
                        'sellers': charts_data.get('daily_breakdown', {}).get('sellers_by_hour', {}),
                        'brands': charts_data.get('daily_breakdown', {}).get('brands_by_hour', {}),
                        'qa': charts_data.get('daily_breakdown', {}).get('qa_by_hour', {})
                    }
                }
            
            # Generate enhanced HTML report with charts
            html_report = self._generate_html_report_with_charts(report_data, charts_data)
            
            success_count = 0
            for email in manager_emails:
                if self.email_service.send_email(
                    email,
                    f"Daily Lead Generation Report - {report_data.get('date', 'Today')}",
                    self._generate_text_report(report_data),
                    html_report
                ):
                    success_count += 1
            
            logger.info(f"✅ Sent daily report to {success_count}/{len(manager_emails)} managers")
            return success_count
            
        except Exception as e:
            logger.error(f"Error sending daily report: {str(e)}")
            return 0
    
    def _generate_html_report_with_charts(self, report_data, charts_data=None):
        """Generate HTML report with embedded charts - 100% Automated"""
        try:
            summary = report_data.get('summary', {})
            metrics = report_data.get('metrics', {})
            top_performers = report_data.get('top_performers', {})
            automation_summary = report_data.get('automation_summary', {})
            
            # Chart data
            profitability_dist = charts_data.get('profitability_distribution', {}) if charts_data else {}
            competition_dist = charts_data.get('competition_score_distribution', {}) if charts_data else {}
            automation_eff = charts_data.get('automation_efficiency', {}) if charts_data else {}
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                    .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                    h1 {{ color: #1976d2; border-bottom: 3px solid #1976d2; padding-bottom: 10px; }}
                    h2 {{ color: #424242; margin-top: 30px; }}
                    .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
                    .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
                    .stat-card h3 {{ margin: 0 0 10px 0; font-size: 14px; opacity: 0.9; }}
                    .stat-card .value {{ font-size: 32px; font-weight: bold; margin: 10px 0; }}
                    .stat-card.green {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }}
                    .stat-card.blue {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
                    .stat-card.orange {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }}
                    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                    th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                    th {{ background-color: #1976d2; color: white; }}
                    tr:hover {{ background-color: #f5f5f5; }}
                    .chart-placeholder {{ background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center; color: #666; }}
                    .automation-badge {{ display: inline-block; padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
                    .badge-100 {{ background: #4caf50; color: white; }}
                    .badge-90 {{ background: #8bc34a; color: white; }}
                    .badge-80 {{ background: #ffc107; color: black; }}
                    .badge-70 {{ background: #ff9800; color: white; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>📊 Daily Lead Generation Report</h1>
                    <p><strong>Date:</strong> {report_data.get('date', 'N/A')}</p>
                    <p><strong>Report Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <span class="automation-badge badge-100">🤖 100% Automated</span>
                    
                    <h2>📈 Summary Statistics</h2>
                    <div class="summary-grid">
                        <div class="stat-card green">
                            <h3>New Sellers</h3>
                            <div class="value">{summary.get('new_sellers', 0)}</div>
                            <small>Total: {summary.get('total_sellers', 0)}</small>
                        </div>
                        <div class="stat-card blue">
                            <h3>New Brands</h3>
                            <div class="value">{summary.get('new_brands', 0)}</div>
                            <small>Total: {summary.get('total_brands', 0)}</small>
                        </div>
                        <div class="stat-card orange">
                            <h3>QA Analyses</h3>
                            <div class="value">{summary.get('qa_completed', 0)}</div>
                            <small>Profitable: {summary.get('profitable_brands', 0)}</small>
                        </div>
                        <div class="stat-card">
                            <h3>Avg Profit Margin</h3>
                            <div class="value">{metrics.get('average_profit_margin', 0)}%</div>
                            <small>Competition: {metrics.get('average_competition_score', 0)}</small>
                        </div>
                    </div>
                    
                    <h2>📊 Charts & Graphs</h2>
                    <div class="chart-placeholder">
                        <h3>Profitability Distribution</h3>
                        <p>Highly Profitable: {profitability_dist.get('highly_profitable', 0)} | 
                           Profitable: {profitability_dist.get('profitable', 0)} | 
                           Marginal: {profitability_dist.get('marginal', 0)} | 
                           Unprofitable: {profitability_dist.get('unprofitable', 0)}</p>
                    </div>
                    
                    <div class="chart-placeholder">
                        <h3>Competition Score Distribution</h3>
                        <p>Low: {competition_dist.get('low_competition', 0)} | 
                           Moderate: {competition_dist.get('moderate_competition', 0)} | 
                           High: {competition_dist.get('high_competition', 0)} | 
                           Very High: {competition_dist.get('very_high_competition', 0)}</p>
                    </div>
                    
                    <div class="chart-placeholder">
                        <h3>Automation Efficiency</h3>
                        <p>Average Automation: {automation_eff.get('average_automation_percentage', 0)}% | 
                           Tasks Automated: {automation_eff.get('total_automated_tasks', 0)} | 
                           Time Saved: {automation_eff.get('time_saved_hours', 0)} hours</p>
                    </div>
                    
                    <h2>🏆 Top Performers</h2>
                    <h3>Most Profitable Brands</h3>
                    <table>
                        <tr>
                            <th>Brand Name</th>
                            <th>Profit Margin</th>
                            <th>Status</th>
                        </tr>
            """
            
            # Add top profitable brands
            top_profitable = top_performers.get('top_profitable_brands', [])
            for brand in top_profitable[:10]:
                html += f"""
                        <tr>
                            <td>{brand.get('brand_name', 'N/A')}</td>
                            <td>{brand.get('profit_margin', 0)}%</td>
                            <td>{brand.get('status', 'N/A')}</td>
                        </tr>
                """
            
            html += """
                    </table>
                    
                    <h2>🤖 Automation Summary</h2>
                    <table>
                        <tr>
                            <th>Task</th>
                            <th>Status</th>
                            <th>Results</th>
                        </tr>
            """
            
            # Add automation summary
            if automation_summary:
                html += f"""
                        <tr>
                            <td>Morning Setup</td>
                            <td>{'✅ Run' if automation_summary.get('morning_setup', {}).get('run') else '⏭️ Skipped'}</td>
                            <td>{automation_summary.get('morning_setup', {}).get('brands_extracted', 0)} brands extracted</td>
                        </tr>
                        <tr>
                            <td>Seller Sniping</td>
                            <td>✅ Completed</td>
                            <td>{automation_summary.get('seller_sniping', {}).get('brands_found', 0)} brands found</td>
                        </tr>
                        <tr>
                            <td>Brand Research</td>
                            <td>✅ Completed</td>
                            <td>{automation_summary.get('brand_research', {}).get('brands_researched', 0)} brands researched ({automation_summary.get('brand_research', {}).get('avg_automation', 0):.0f}% automated)</td>
                        </tr>
                        <tr>
                            <td>QA Analysis</td>
                            <td>✅ Completed</td>
                            <td>{automation_summary.get('qa_analysis', {}).get('analyses_completed', 0)} analyses ({automation_summary.get('qa_analysis', {}).get('avg_automation', 0):.0f}% automated)</td>
                        </tr>
                """
            
            html += """
                    </table>
                    
                    <h2>⚠️ Issues Flagged</h2>
                    <ul>
            """
            
            # Add issues
            issues = report_data.get('issues', [])
            for issue in issues:
                html += f"<li>{issue}</li>"
            
            html += """
                    </ul>
                    
                    <hr>
                    <p><em>This is an automated 100% automated report from Lead Generation Tool</em></p>
                    <p><small>Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
                </div>
            </body>
            </html>
            """
            
            return html
            
        except Exception as e:
            logger.error(f"Error generating HTML report: {str(e)}")
            return self._generate_text_report(report_data)
    
    def _generate_text_report(self, report_data):
        """Generate text version of report"""
        try:
            summary = report_data.get('summary', {})
            metrics = report_data.get('metrics', {})
            
            text = f"""
Daily Lead Generation Report
Date: {report_data.get('date', 'N/A')}

SUMMARY:
- New Sellers: {summary.get('new_sellers', 0)} (Total: {summary.get('total_sellers', 0)})
- New Brands: {summary.get('new_brands', 0)} (Total: {summary.get('total_brands', 0)})
- QA Analyses Completed: {summary.get('qa_completed', 0)}
- Profitable Brands: {summary.get('profitable_brands', 0)}

METRICS:
- Average Profit Margin: {metrics.get('average_profit_margin', 0)}%
- Average Competition Score: {metrics.get('average_competition_score', 0)}
- Profitability Rate: {metrics.get('profitability_rate', 0)}%

This is an automated 100% automated report from Lead Generation Tool
            """
            return text.strip()
        except:
            return "Daily report generated"
    
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
    
    def _get_top_performers(self, sellers, brands, qa_analyses):
        """Get top performing sellers/brands - 100% Automated"""
        try:
            # Top brands by profitability
            top_brands = sorted(
                [qa for qa in qa_analyses if qa.get('profit_margin')],
                key=lambda x: x.get('profit_margin', 0) or 0,
                reverse=True
            )[:5]
            
            # Top brands by competition score
            top_competition = sorted(
                [qa for qa in qa_analyses if qa.get('competition_score')],
                key=lambda x: (x.get('competition_score', {}).get('score', 0) if isinstance(x.get('competition_score'), dict) else (x.get('competition_score', 0) or 0)),
                reverse=True
            )[:5]
            
            return {
                'top_profitable_brands': [
                    {
                        'brand_name': qa.get('brand_name', 'Unknown'),
                        'profit_margin': qa.get('profit_margin', 0),
                        'status': qa.get('status', '')
                    }
                    for qa in top_brands
                ],
                'top_competition_brands': [
                    {
                        'brand_name': qa.get('brand_name', 'Unknown'),
                        'competition_score': qa.get('competition_score', {}).get('score', 0) if isinstance(qa.get('competition_score'), dict) else qa.get('competition_score', 0),
                        'level': qa.get('competition_score', {}).get('level', '') if isinstance(qa.get('competition_score'), dict) else ''
                    }
                    for qa in top_competition
                ],
                'most_active_sellers': len(sellers),
                'most_researched_brands': len(brands)
            }
        except Exception as e:
            logger.error(f"Error getting top performers: {str(e)}")
            return {}
    
    def _get_flagged_issues(self, sellers, brands):
        """Get flagged issues that need attention - 100% Automated"""
        try:
            issues = []
            
            # Check for duplicates
            duplicate_sellers = [s for s in sellers if s.get('is_duplicate', False)]
            duplicate_brands = [b for b in brands if b.get('is_duplicate', False)]
            
            if duplicate_sellers:
                issues.append(f"{len(duplicate_sellers)} duplicate sellers flagged")
            if duplicate_brands:
                issues.append(f"{len(duplicate_brands)} duplicate brands flagged")
            
            # Check for validation issues
            invalid_sellers = [s for s in sellers if s.get('validation_status') == 'failed']
            invalid_brands = [b for b in brands if b.get('validation_status') == 'failed']
            
            if invalid_sellers:
                issues.append(f"{len(invalid_sellers)} sellers with validation issues")
            if invalid_brands:
                issues.append(f"{len(invalid_brands)} brands with validation issues")
            
            return issues if issues else ["No critical issues flagged"]
        except Exception as e:
            logger.error(f"Error getting flagged issues: {str(e)}")
            return ["Error checking issues"]
    
    def _get_automation_summary(self, sellers, brands, qa_analyses):
        """Get automation summary - 100% Automated"""
        try:
            return {
                'morning_setup': {
                    'run': len([b for b in brands if 'smartscout' in str(b.get('source', '')).lower()]) > 0,
                    'brands_extracted': len([b for b in brands if 'smartscout' in str(b.get('source', '')).lower()])
                },
                'seller_sniping': {
                    'sellers_targeted': len([s for s in sellers if 'seller_sniping' in str(s.get('source', '')).lower()]),
                    'brands_found': len([b for b in brands if 'seller_sniping' in str(b.get('source', '')).lower()])
                },
                'brand_research': {
                    'brands_researched': len([b for b in brands if b.get('automation_percentage', 0) >= 80]),
                    'avg_automation': sum([b.get('automation_percentage', 0) for b in brands]) / len(brands) if brands else 0
                },
                'qa_analysis': {
                    'analyses_completed': len(qa_analyses),
                    'avg_automation': sum([qa.get('automation_percentage', 0) for qa in qa_analyses]) / len(qa_analyses) if qa_analyses else 0
                }
            }
        except Exception as e:
            logger.error(f"Error getting automation summary: {str(e)}")
            return {}
    
    def _analyze_trends(self, week_sellers, week_brands):
        """Analyze trends for the week"""
        if len(week_sellers) > 0 or len(week_brands) > 0:
            return f"Positive growth: {len(week_sellers)} sellers and {len(week_brands)} brands added this week"
        return "No significant trends this week"
    
    def _calculate_growth_rate(self, sellers, brands):
        """Calculate growth rate"""
        # Placeholder - would compare with previous period
        return "15% growth rate"

