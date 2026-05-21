from ..extensions import db
from ..model.Project import Project

'''
Нужно доделать сервисы TeamService и ProjectService.
'''

class ProjectService:
    @staticmethod
    def get_project(proj_id):
        project = Project.query.get(proj_id)
        if project is None:
            raise ValueError(f"Project with id {proj_id} not found") 
        return project
    
    @staticmethod
    def get_all_projects():
        return Project.query.all()
    
    @staticmethod
    def get_projects(user_id):
        pass