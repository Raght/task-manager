from ..extensions import db
from ..model.Tasks import Task
from ..model.Users import Users
from ..model.Enums import TaskStatus, TaskPriority


class TaskService():
    @staticmethod
    def _resolve_status(status):
        if status is None:
            return None
        if isinstance(status, int):
            return TaskStatus.query.get(status)
        return TaskStatus.query.filter_by(name=status).first()

    @staticmethod
    def _resolve_priority(priority):
        if priority is None:
            return None
        if isinstance(priority, int):
            return TaskPriority.query.get(priority)
        return TaskPriority.query.filter_by(name=priority).first()

    @staticmethod
    def get_task(task_id):
        task = Task.query.get(task_id)
        if task is None:
            raise ValueError(f"Task with id {task_id} not found")
        return task

    @staticmethod
    def create_task(data):
        if not isinstance(data, dict):
            raise ValueError('Task data must be provided as a dictionary')

        required_fields = ['name', 'createdBy', 'projectID']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required to create a task")

        status = TaskService._resolve_status(data.get('statusID') or data.get('status'))
        priority = TaskService._resolve_priority(data.get('priorityID') or data.get('priority'))

        if data.get('assignedTo') is not None and not Users.query.get(data.get('assignedTo')):
            raise ValueError(f"Assigned user with id {data.get('assignedTo')} does not exist")

        task = Task(
            name=data.get('name'),
            description=data.get('description'),
            createdBy=data.get('createdBy'),
            deadline=data.get('deadline'),
            statusID=status.id if status else None,
            priorityID=priority.id if priority else None,
            assignedTo=data.get('assignedTo'),
            projectID=data.get('projectID')
        )

        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def update_task(task_id, data):
        if not isinstance(data, dict):
            raise ValueError('Task update data must be provided as a dictionary')

        task = TaskService.get_task(task_id)
        allowed_fields = ['name', 'description', 'deadline', 'assignedTo', 'projectID']

        if 'statusID' in data or 'status' in data:
            status = TaskService._resolve_status(data.get('statusID') or data.get('status'))
            if status is None:
                raise ValueError('Invalid status value provided')
            task.statusID = status.id

        if 'priorityID' in data or 'priority' in data:
            priority = TaskService._resolve_priority(data.get('priorityID') or data.get('priority'))
            if priority is None:
                raise ValueError('Invalid priority value provided')
            task.priorityID = priority.id

        if 'assignedTo' in data and data.get('assignedTo') is not None:
            if not Users.query.get(data.get('assignedTo')):
                raise ValueError(f"Assigned user with id {data.get('assignedTo')} does not exist")
            task.assignedTo = data.get('assignedTo')

        for field in allowed_fields:
            if field in data:
                setattr(task, field, data.get(field))

        db.session.commit()
        return task
    
    @staticmethod
    def remove_task(task_id):
        task = TaskService.get_task(task_id)
        Task.query.delete(task)
        db.session.commit()

    @staticmethod
    def change_status(task_id, status):
        task = TaskService.get_task(task_id)
        status_obj = TaskService._resolve_status(status)
        if status_obj is None:
            raise ValueError('Invalid task status')
        task.statusID = status_obj.id
        db.session.commit()
        return task

    @staticmethod
    def change_priority(task_id, priority):
        task = TaskService.get_task(task_id)
        priority_obj = TaskService._resolve_priority(priority)
        if priority_obj is None:
            raise ValueError('Invalid task priority')
        task.priorityID = priority_obj.id
        db.session.commit()
        return task

    @staticmethod
    def assign_task(task_id, user_id):
        task = TaskService.get_task(task_id)
        if user_id is not None and not Users.query.get(user_id):
            raise ValueError(f"User with id {user_id} does not exist")
        task.assignedTo = user_id
        db.session.commit()
        return task

    @staticmethod
    def filter_tasks(filters=None):
        filters = filters or {}
        query = Task.query

        if filters.get('statusID') is not None or filters.get('status') is not None:
            status = TaskService._resolve_status(filters.get('statusID') or filters.get('status'))
            if status is None:
                raise ValueError('Invalid status filter')
            query = query.filter_by(statusID=status.id)

        if filters.get('priorityID') is not None or filters.get('priority') is not None:
            priority = TaskService._resolve_priority(filters.get('priorityID') or filters.get('priority'))
            if priority is None:
                raise ValueError('Invalid priority filter')
            query = query.filter_by(priorityID=priority.id)

        if filters.get('assignedTo') is not None:
            query = query.filter_by(assignedTo=filters.get('assignedTo'))

        if filters.get('createdBy') is not None:
            query = query.filter_by(createdBy=filters.get('createdBy'))

        if filters.get('projectID') is not None:
            query = query.filter_by(projectID=filters.get('projectID'))

        if filters.get('deadline_before') is not None:
            query = query.filter(Task.deadline <= filters.get('deadline_before'))

        if filters.get('deadline_after') is not None:
            query = query.filter(Task.deadline >= filters.get('deadline_after'))

        return query.all()

    @staticmethod
    def get_tasks_created_by_user(user_id):
        return Task.query.filter_by(createdBy=user_id).all()

    @staticmethod
    def get_tasks_assigned_to_user(user_id):
        return Task.query.filter_by(assignedTo=user_id).all()
