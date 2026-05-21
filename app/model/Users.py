from ..extensions import db
from flask_login import UserMixin
from datetime import datetime, timezone

# Association table for Team-User many-to-many relationship
team_user = db.Table(
    'team_user',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Users(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    notificationTypeID = db.Column(db.Integer, db.ForeignKey('notification_type.id'))
    
    # Relationships
    teams = db.relationship('Team', secondary=team_user, backref=db.backref('users', lazy=True))
    projects = db.relationship('Project', backref='creator', lazy=True, foreign_keys='Project.createdBy')
    tasks_created = db.relationship('Task', backref='creator', lazy=True, foreign_keys='Task.createdBy')
    tasks_assigned = db.relationship('Task', backref='assignee', lazy=True, foreign_keys='Task.assignedTo')
    notificationType = db.relationship('NotificationType', lazy=True)

    def __repr__(self):
        return f'User <id:{self.id}> {self.name} {self.email}'