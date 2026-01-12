from app.models.database import db
from datetime import datetime
import uuid
import json

class AuditLog(db.Model):
    """Audit log model for tracking user actions"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True, index=True)
    action = db.Column(db.String(50), nullable=False, index=True)  # create, update, delete, login, logout
    entity_type = db.Column(db.String(50), nullable=True, index=True)  # seller, brand, qa_analysis, user
    entity_id = db.Column(db.String(36), nullable=True, index=True)
    description = db.Column(db.Text, nullable=True)
    changes = db.Column(db.Text, nullable=True)  # JSON string for before/after changes
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def set_changes(self, changes_dict):
        """Set changes as JSON string"""
        if changes_dict:
            self.changes = json.dumps(changes_dict)
        else:
            self.changes = None
    
    def get_changes(self):
        """Get changes as dictionary"""
        if self.changes:
            try:
                return json.loads(self.changes)
            except:
                return {}
        return {}
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'description': self.description,
            'changes': self.get_changes(),
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_id}>'

