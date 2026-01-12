from app.models.database import db
from datetime import datetime
import uuid
import json

class QAAnalysis(db.Model):
    """QA Analysis model"""
    __tablename__ = 'qa_analyses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    brand_id = db.Column(db.String(36), db.ForeignKey('brands.id'), nullable=False, index=True)
    brand_name = db.Column(db.String(200), nullable=True)
    profit_margin = db.Column(db.Float, nullable=True)
    average_price = db.Column(db.Float, nullable=True)
    min_price = db.Column(db.Float, nullable=True)
    max_price = db.Column(db.Float, nullable=True)
    product_count = db.Column(db.Integer, default=0)
    competition_score = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default='unprofitable', nullable=False)  # profitable, unprofitable
    analysis_data = db.Column(db.Text, nullable=True)  # JSON string for additional data
    notes = db.Column(db.Text, nullable=True)
    analyzed_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    analyzer = db.relationship('User', foreign_keys=[analyzed_by], lazy=True)
    
    def set_analysis_data(self, data_dict):
        """Set analysis data as JSON string"""
        if data_dict:
            self.analysis_data = json.dumps(data_dict)
        else:
            self.analysis_data = None
    
    def get_analysis_data(self):
        """Get analysis data as dictionary"""
        if self.analysis_data:
            try:
                return json.loads(self.analysis_data)
            except:
                return {}
        return {}
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'brand_id': self.brand_id,
            'brand_name': self.brand_name,
            'profit_margin': self.profit_margin,
            'average_price': self.average_price,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'product_count': self.product_count,
            'competition_score': self.competition_score,
            'status': self.status,
            'analysis_data': self.get_analysis_data(),
            'notes': self.notes,
            'analyzed_by': self.analyzed_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<QAAnalysis {self.brand_name}>'

