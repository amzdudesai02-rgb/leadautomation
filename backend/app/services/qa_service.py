from app.scrapers.qa_analyzer import QAAnalyzer
from app.services.database_service import DatabaseService
from app.utils.logger import get_logger
import time

logger = get_logger(__name__)

class QAService:
    def __init__(self):
        self.analyzer = QAAnalyzer()
        self.db_service = DatabaseService()
    
    def analyze_brand(self, brand_id, user_id=None):
        """Perform QA analysis on a brand"""
        try:
            logger.info(f"Analyzing brand: {brand_id}")
            
            # Get brand data
            brand = self.db_service.get_brand_by_id(brand_id)
            if not brand:
                raise ValueError(f"Brand {brand_id} not found")
            
            # Perform analysis
            analysis = self.analyzer.analyze(brand)
            
            # Save analysis results
            saved_analysis = self.db_service.save_qa_analysis(brand_id, analysis, user_id)
            
            logger.info(f"QA analysis completed for brand: {brand_id}")
            return saved_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing brand: {str(e)}")
            raise
    
    def get_metrics(self, brand_id):
        """Get QA metrics for a brand"""
        try:
            metrics = self.db_service.get_qa_metrics(brand_id)
            return metrics
        except Exception as e:
            logger.error(f"Error fetching QA metrics: {str(e)}")
            raise

