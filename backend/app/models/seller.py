from app.models.database import db
from datetime import datetime
import uuid

class Seller(db.Model):
    """Seller model"""
    __tablename__ = 'sellers'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=True, index=True)
    store_url = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    company_name = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    total_reviews = db.Column(db.Integer, default=0)
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
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'store_url': self.store_url,
            'phone': self.phone,
            'company_name': self.company_name,
            'location': self.location,
            'rating': self.rating,
            'total_reviews': self.total_reviews,
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
        return f'<Seller {self.name}>'

