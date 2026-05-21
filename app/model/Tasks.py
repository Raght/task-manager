from ..extensions import db
from datetime import datetime, timezone

class Task(db.Model):
    __tablename__ = 'task'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(2000))
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    createdBy = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    deadline = db.Column(db.DateTime)
    statusID = db.Column(db.Integer, db.ForeignKey('task_status.id'))
    priorityID = db.Column(db.Integer, db.ForeignKey('task_priority.id'))
    assignedTo = db.Column(db.Integer, db.ForeignKey('user.id'))
    projectID = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    
    # Relationships
    status = db.relationship('TaskStatus', lazy=True)
    priority = db.relationship('TaskPriority', lazy=True)

    def __repr__(self):
        return f'Task <{self.id}>: {self.name} | {self.status}'