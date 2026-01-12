from app.models.database import db
from datetime import datetime
import uuid
import json

class Brand(db.Model):
    """Brand model"""
    __tablename__ = 'brands'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False, index=True)
    domain = db.Column(db.String(255), nullable=True, index=True)
    email = db.Column(db.String(120), nullable=True, index=True)
    phone = db.Column(db.String(20), nullable=True)
    social_media = db.Column(db.Text, nullable=True)  # JSON string
    description = db.Column(db.Text, nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='active', nullable=False)  # active, inactive, flagged
    is_duplicate = db.Column(db.Boolean, default=False, nullable=False)
    validation_status = db.Column(db.String(20), default='pending', nullable=False)  # valid, invalid, pending
    validation_issues = db.Column(db.Text, nullable=True)  # JSON string
    notes = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by], lazy=True)
    qa_analyses = db.relationship('QAAnalysis', backref='brand', lazy=True, cascade='all, delete-orphan')
    
    def set_social_media(self, social_dict):
        """Set social media as JSON string"""
        if social_dict:
            self.social_media = json.dumps(social_dict)
        else:
            self.social_media = None
    
    def get_social_media(self):
        """Get social media as dictionary"""
        if self.social_media:
            try:
                return json.loads(self.social_media)
            except:
                return {}
        return {}
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'email': self.email,
            'phone': self.phone,
            'social_media': self.get_social_media(),
            'description': self.description,
            'industry': self.industry,
            'location': self.location,
            'status': self.status,
            'is_duplicate': self.is_duplicate,
            'validation_status': self.validation_status,
            'validation_issues': self.validation_issues,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Brand {self.name}>'

