from ..extensions import db
from ..model.Users import Users

class TeamService:
    @staticmethod
    def get_all():
        return Users.query.all()
    
    @staticmethod
    def get_team(team_id):
        team = Users.query.get(team_id)
        if team is None:
            raise ValueError(f"Team with id {team_id} not found")  
        return team
    
    @staticmethod
    def add_team():
        pass

    @staticmethod
    def update_team():
        pass

    @staticmethod
    def remove_team():
        pass

    ...