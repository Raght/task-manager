import datetime
from .TeamService import TeamService
from ..extensions import db
from ..model import Team
from ..model.Project import Project
from ..model.Users import Users
from ..model.Team import Team
from ..model.Enums import ProjectStatus
from .TaskSortStrategy import SORT_STRATEGIES

class ProjectService:
    @staticmethod
    def _resolve_status(status):
        if status is None:
            return None
        if isinstance(status, int):
            return ProjectStatus.query.get(status)
        return ProjectStatus.query.filter_by(name=status).first()

    @staticmethod
    def get_project(proj_id):
        project = Project.query.get(proj_id)
        if project is None:
            raise ValueError(f"Project with id {proj_id} not found") 
        return project

    @staticmethod
    def get_projects(project_ids):
        projects = Project.query.get(Project.id.in_(project_ids)).all()
        return projects

    @staticmethod
    def get_all_statuses():
        return ProjectStatus.query.order_by(ProjectStatus.id).all()

    @staticmethod
    def get_all_projects():
        return Project.query.all()
    
    @staticmethod
    def get_user_projects(user_id):
        return Project.query.filter_by(createdBy=user_id).all()

    @staticmethod
    def get_participation_projects(user_id):
        teams = TeamService.get_participating_teams(user_id)
        project_ids = [team.projectID for team in teams]
        projects = Project.query.filter(Project.id.in_(project_ids)).all()

        return projects
    
    @staticmethod
    def create_project(data):
        if not isinstance(data, dict):
            raise ValueError('Project data must be provided as a dictionary')

        required_fields = ['name', 'createdBy', 'status']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required to create a project")

        if not Users.query.get(data.get('createdBy')):
            raise ValueError(f"User with id {data.get('createdBy')} does not exist")

        status = ProjectService._resolve_status(data.get('statusID') or data.get('status'))

        project = Project(
            name=data.get('name'),
            description=data.get('description'),
            createdBy=data.get('createdBy'),
            createdAt=datetime.datetime.now(datetime.timezone.utc),
            statusID=status.id if status else None
        )

        db.session.add(project)
        db.session.commit()
        return project

    @staticmethod
    def update_project(project_id, data):
        if not isinstance(data, dict):
            raise ValueError('Project data must be provided as a dictionary')

        required_fields = ['name', 'createdBy', 'status']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required to create a project")

        if not Users.query.get(data.get('createdBy')):
            raise ValueError(f"User with id {data.get('createdBy')} does not exist")

        project = ProjectService.get_project(project_id)

        allowed_fields = ['name', 'description']

        if 'statusID' in data or 'status' in data:
            status = ProjectService._resolve_status(data.get('statusID') or data.get('status'))
            if status is None:
                raise ValueError('Invalid status value provided')
            project.statusID = status.id

        for field in allowed_fields:
            if field in data:
                setattr(project, field, data.get(field))

        db.session.commit()
        return project

    @staticmethod
    def delete_project(proj_id):
        project = ProjectService.get_project(proj_id)
        db.session.delete(project)
        db.session.commit()

    @staticmethod
    def change_status(proj_id, status):
        project = ProjectService.get_project(proj_id)
        status_obj = ProjectService._resolve_status(status)
        if status_obj is None:
            raise ValueError('Invalid project status')
        project.statusID = status_obj.id
        db.session.commit()
        return project

    @staticmethod
    def get_sorted_tasks(proj_id, sort='id', order='asc'):
        project = ProjectService.get_project(proj_id)
        strategy = SORT_STRATEGIES.get(sort)
        if strategy is None:
            raise ValueError(f"Invalid sort key: {sort}")
        if order not in ('asc', 'desc'):
            raise ValueError(f"Invalid sort order: {order}")
        return strategy.apply(list(project.tasks), reverse=(order == 'desc'))

    @staticmethod
    def get_available_sorts():
        return list(SORT_STRATEGIES.keys())