from .Users import Users, team_user
from .Tasks import Task
from .Project import Project
from .Team import Team
from .Enums import (
    NotificationType, ProjectStatus, TaskStatus, TaskPriority,
    NotificationTypeEnum, ProjectStatusEnum, TaskStatusEnum, TaskPriorityEnum
)

__all__ = [
    'Users',
    'Task',
    'Project',
    'Team',
    'team_user',
    'NotificationType',
    'ProjectStatus',
    'TaskStatus',
    'TaskPriority',
    'NotificationTypeEnum',
    'ProjectStatusEnum',
    'TaskStatusEnum',
    'TaskPriorityEnum',
]


def init_enum_tables(db):
    """Initialize enum tables with default values."""
    from .Enums import (
        NotificationTypeEnum, ProjectStatusEnum, 
        TaskStatusEnum, TaskPriorityEnum
    )
    
    # Notification Types
    for enum_val in NotificationTypeEnum:
        if not NotificationType.query.filter_by(name=enum_val.value).first():
            db.session.add(NotificationType(name=enum_val.value))
    
    # Project Statuses
    for enum_val in ProjectStatusEnum:
        if not ProjectStatus.query.filter_by(name=enum_val.value).first():
            db.session.add(ProjectStatus(name=enum_val.value))
    
    # Task Statuses
    for enum_val in TaskStatusEnum:
        if not TaskStatus.query.filter_by(name=enum_val.value).first():
            db.session.add(TaskStatus(name=enum_val.value))
    
    # Task Priorities
    for enum_val in TaskPriorityEnum:
        if not TaskPriority.query.filter_by(name=enum_val.value).first():
            db.session.add(TaskPriority(name=enum_val.value))
    
    db.session.commit()

