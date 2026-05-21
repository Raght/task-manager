from ..extensions import db
from enum import Enum

# Python Enums for code convenience
class NotificationTypeEnum(str, Enum):
    EMAIL = "EMAIL"
    IN_APP = "IN_APP"

class ProjectStatusEnum(str, Enum):
    PLANNING = "PLANNING"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class TaskStatusEnum(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    DONE = "DONE"

class TaskPriorityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# Database Models for enum tables
class NotificationType(db.Model):
    __tablename__ = 'notification_type'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f"{self.name}"


class ProjectStatus(db.Model):
    __tablename__ = 'project_status'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f"{self.name}"


class TaskStatus(db.Model):
    __tablename__ = 'task_status'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f"{self.name}"


class TaskPriority(db.Model):
    __tablename__ = 'task_priority'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f"{self.name}"

