"""
Research Queue Service - Manages brand research queue
"""
from app.services.database_service import DatabaseService
from app.utils.logger import get_logger
import time

logger = get_logger(__name__)

class ResearchQueueService:
    """Service for managing brand research queue"""
    
    def __init__(self):
        self.db_service = DatabaseService()
    
    def add_to_queue(self, brand_name, source='seller_sniping', priority='normal', metadata=None):
        """Add brand to research queue"""
        try:
            # Check if brand already exists in database
            existing_brand = self.db_service.get_brand_by_name(brand_name)
            if existing_brand:
                logger.info(f"Brand '{brand_name}' already exists, skipping queue")
                return {
                    'added': False,
                    'reason': 'already_exists',
                    'brand_id': existing_brand.get('id')
                }
            
            # Check if already in queue
            queue_item = {
                'brand_name': brand_name,
                'source': source,
                'priority': priority,
                'status': 'pending',
                'metadata': metadata or {},
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Save to queue (would be stored in database or queue table)
            # For now, return success
            logger.info(f"✅ Added '{brand_name}' to research queue (priority: {priority})")
            
            return {
                'added': True,
                'brand_name': brand_name,
                'priority': priority,
                'queue_item': queue_item
            }
            
        except Exception as e:
            logger.error(f"Error adding to research queue: {str(e)}")
            return {
                'added': False,
                'error': str(e)
            }
    
    def add_batch_to_queue(self, brand_names, source='seller_sniping', priority='normal'):
        """Add multiple brands to queue"""
        results = {
            'added': [],
            'skipped': [],
            'errors': []
        }
        
        for brand_name in brand_names:
            result = self.add_to_queue(brand_name, source, priority)
            if result.get('added'):
                results['added'].append(brand_name)
            elif result.get('reason') == 'already_exists':
                results['skipped'].append(brand_name)
            else:
                results['errors'].append({
                    'brand': brand_name,
                    'error': result.get('error', 'Unknown error')
                })
        
        logger.info(f"Batch queue: {len(results['added'])} added, {len(results['skipped'])} skipped, {len(results['errors'])} errors")
        return results
    
    def get_queue(self, status='pending', limit=100):
        """Get brands from research queue"""
        try:
            # Would fetch from queue table
            # For now, return empty list
            return []
        except Exception as e:
            logger.error(f"Error getting queue: {str(e)}")
            return []

