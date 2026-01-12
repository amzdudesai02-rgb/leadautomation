import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from app.config import Config
from app.utils.logger import get_logger
import os

logger = get_logger(__name__)

class EmailService:
    """Service for sending emails via Gmail API/SMTP"""
    
    def __init__(self):
        self.gmail_user = Config.GMAIL_USER
        self.gmail_password = Config.GMAIL_PASSWORD
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
    
    def send_email(self, to_email, subject, body, html_body=None, attachments=None):
        """Send email via SMTP"""
        try:
            if not self.gmail_user or not self.gmail_password:
                logger.warning("Gmail credentials not configured")
                return False
            
            msg = MIMEMultipart('alternative')
            msg['From'] = self.gmail_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add text and HTML parts
            if html_body:
                text_part = MIMEText(body, 'plain')
                html_part = MIMEText(html_body, 'html')
                msg.attach(text_part)
                msg.attach(html_part)
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments if any
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_daily_report(self, to_email, report_data):
        """Send daily report email"""
        try:
            subject = f"Daily Lead Generation Report - {report_data.get('date', 'Today')}"
            
            html_body = f"""
            <html>
            <body>
                <h2>Daily Lead Generation Report</h2>
                <p><strong>Date:</strong> {report_data.get('date', 'N/A')}</p>
                
                <h3>Summary</h3>
                <ul>
                    <li><strong>New Sellers:</strong> {report_data.get('new_sellers', 0)}</li>
                    <li><strong>New Brands:</strong> {report_data.get('new_brands', 0)}</li>
                    <li><strong>QA Analyses Completed:</strong> {report_data.get('qa_completed', 0)}</li>
                    <li><strong>Total Sellers:</strong> {report_data.get('total_sellers', 0)}</li>
                    <li><strong>Total Brands:</strong> {report_data.get('total_brands', 0)}</li>
                </ul>
                
                <h3>Top Performers</h3>
                <p>{report_data.get('top_performers', 'N/A')}</p>
                
                <h3>Issues Flagged</h3>
                <p>{report_data.get('issues', 'None')}</p>
                
                <hr>
                <p><em>This is an automated report from Lead Generation Tool</em></p>
            </body>
            </html>
            """
            
            text_body = f"""
            Daily Lead Generation Report
            Date: {report_data.get('date', 'N/A')}
            
            Summary:
            - New Sellers: {report_data.get('new_sellers', 0)}
            - New Brands: {report_data.get('new_brands', 0)}
            - QA Analyses Completed: {report_data.get('qa_completed', 0)}
            - Total Sellers: {report_data.get('total_sellers', 0)}
            - Total Brands: {report_data.get('total_brands', 0)}
            
            Top Performers: {report_data.get('top_performers', 'N/A')}
            Issues Flagged: {report_data.get('issues', 'None')}
            """
            
            return self.send_email(to_email, subject, text_body, html_body)
            
        except Exception as e:
            logger.error(f"Error sending daily report: {str(e)}")
            return False
    
    def send_weekly_summary(self, to_email, summary_data):
        """Send weekly summary email"""
        try:
            subject = f"Weekly Lead Generation Summary - Week of {summary_data.get('week_start', 'N/A')}"
            
            html_body = f"""
            <html>
            <body>
                <h2>Weekly Lead Generation Summary</h2>
                <p><strong>Week:</strong> {summary_data.get('week_start', 'N/A')} to {summary_data.get('week_end', 'N/A')}</p>
                
                <h3>Weekly Statistics</h3>
                <ul>
                    <li><strong>Total New Sellers:</strong> {summary_data.get('total_new_sellers', 0)}</li>
                    <li><strong>Total New Brands:</strong> {summary_data.get('total_new_brands', 0)}</li>
                    <li><strong>Total QA Analyses:</strong> {summary_data.get('total_qa', 0)}</li>
                    <li><strong>Average Profit Margin:</strong> {summary_data.get('avg_profit_margin', 0)}%</li>
                    <li><strong>Top Competition Score:</strong> {summary_data.get('top_competition_score', 0)}</li>
                </ul>
                
                <h3>Trends</h3>
                <p>{summary_data.get('trends', 'N/A')}</p>
                
                <hr>
                <p><em>This is an automated weekly summary from Lead Generation Tool</em></p>
            </body>
            </html>
            """
            
            text_body = f"""
            Weekly Lead Generation Summary
            Week: {summary_data.get('week_start', 'N/A')} to {summary_data.get('week_end', 'N/A')}
            
            Weekly Statistics:
            - Total New Sellers: {summary_data.get('total_new_sellers', 0)}
            - Total New Brands: {summary_data.get('total_new_brands', 0)}
            - Total QA Analyses: {summary_data.get('total_qa', 0)}
            - Average Profit Margin: {summary_data.get('avg_profit_margin', 0)}%
            - Top Competition Score: {summary_data.get('top_competition_score', 0)}
            
            Trends: {summary_data.get('trends', 'N/A')}
            """
            
            return self.send_email(to_email, subject, text_body, html_body)
            
        except Exception as e:
            logger.error(f"Error sending weekly summary: {str(e)}")
            return False

