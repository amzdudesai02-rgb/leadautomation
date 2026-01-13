from apscheduler.schedulers.background import BackgroundScheduler
from app.services.automation_service import AutomationService
from app.services.reporting_service import ReportingService
from app.services.backup_service import BackupService
from app.config import Config
from app.utils.logger import get_logger
import atexit

logger = get_logger(__name__)

class TaskScheduler:
    """Scheduler for automated tasks"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.automation_service = AutomationService()
        self.reporting_service = ReportingService()
        self.backup_service = BackupService()
        self._setup_jobs()
    
    def _setup_jobs(self):
        """Setup scheduled jobs"""
        try:
            # Morning setup - Run at 9:00 AM daily
            self.scheduler.add_job(
                func=self._morning_setup_job,
                trigger='cron',
                hour=9,
                minute=0,
                id='morning_setup',
                name='Morning Setup Automation',
                replace_existing=True
            )
            
            # End of day tasks - Run at 6:00 PM daily
            self.scheduler.add_job(
                func=self._end_of_day_job,
                trigger='cron',
                hour=18,
                minute=0,
                id='end_of_day',
                name='End of Day Automation',
                replace_existing=True
            )
            
            # Daily backup - Run at 11:00 PM daily
            self.scheduler.add_job(
                func=self._backup_job,
                trigger='cron',
                hour=23,
                minute=0,
                id='daily_backup',
                name='Daily Data Backup',
                replace_existing=True
            )
            
            # Weekly summary - Run every Monday at 9:00 AM
            self.scheduler.add_job(
                func=self._weekly_summary_job,
                trigger='cron',
                day_of_week='mon',
                hour=9,
                minute=0,
                id='weekly_summary',
                name='Weekly Summary Report',
                replace_existing=True
            )
            
            logger.info("Scheduled tasks configured")
            
        except Exception as e:
            logger.error(f"Error setting up scheduled jobs: {str(e)}")
    
    def _morning_setup_job(self):
        """Morning setup job"""
        try:
            logger.info("Running scheduled morning setup...")
            self.automation_service.morning_setup()
        except Exception as e:
            logger.error(f"Error in morning setup job: {str(e)}")
    
    def _end_of_day_job(self):
        """End of day job"""
        try:
            logger.info("Running scheduled end of day tasks...")
            self.automation_service.end_of_day_tasks()
        except Exception as e:
            logger.error(f"Error in end of day job: {str(e)}")
    
    def _backup_job(self):
        """Backup job"""
        try:
            logger.info("Running scheduled backup...")
            self.backup_service.backup_all_data()
        except Exception as e:
            logger.error(f"Error in backup job: {str(e)}")
    
    def _weekly_summary_job(self):
        """Weekly summary job"""
        try:
            logger.info("Running scheduled weekly summary...")
            # Get manager emails from config
            manager_emails = Config.MANAGER_EMAILS if hasattr(Config, 'MANAGER_EMAILS') and Config.MANAGER_EMAILS else []
            if manager_emails:
                self.reporting_service.send_weekly_summary_to_managers(manager_emails)
            else:
                logger.warning("No manager emails configured for weekly summary")
        except Exception as e:
            logger.error(f"Error in weekly summary job: {str(e)}")
    
    def start(self):
        """Start the scheduler"""
        try:
            self.scheduler.start()
            logger.info("Task scheduler started")
        except Exception as e:
            logger.error(f"Error starting scheduler: {str(e)}")
    
    def shutdown(self):
        """Shutdown the scheduler"""
        try:
            self.scheduler.shutdown()
            logger.info("Task scheduler stopped")
        except Exception as e:
            logger.error(f"Error shutting down scheduler: {str(e)}")

# Global scheduler instance
scheduler = None

def init_scheduler():
    """Initialize scheduler"""
    global scheduler
    if scheduler is None:
        scheduler = TaskScheduler()
        scheduler.start()
        # Register shutdown handler
        atexit.register(lambda: scheduler.shutdown() if scheduler else None)
    return scheduler

