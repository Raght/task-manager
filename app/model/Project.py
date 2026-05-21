from ..extensions import db
from datetime import datetime, timezone

class Project(db.Model):
    __tablename__ = 'project'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    createdBy = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    statusID = db.Column(db.Integer, db.ForeignKey('project_status.id'))
    
    # Relationships
    teams = db.relationship('Team', backref='project', lazy=True)
    tasks = db.relationship('Task', backref='project', lazy=True)
    status = db.relationship('ProjectStatus', lazy=True)
