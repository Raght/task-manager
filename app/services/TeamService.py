from ..extensions import db
from ..model.Users import Users
from ..model.Project import Project
from ..model.Team import Team


class TeamService:
    @staticmethod
    def create_team(data):
        if not isinstance(data, dict):
            raise ValueError('Project data must be provided as a dictionary')

        required_fields = ['name', 'projectID']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required to create a team")

        team = Team(
            name=data.get('name'),
            projectID=data.get('projectID')
        )

        db.session.add(team)
        db.session.commit()
        return team

    @staticmethod
    def get_team(id):
        team = Team.query.get(id)
        if not team:
            raise ValueError(f"No team with id {id} exists")
        return team

    @staticmethod
    def add_member_to_team(data):
        if not isinstance(data, dict):
            raise ValueError('Data must be provided as a dictionary')

        required_fields = ['id', 'user_id']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required to create a team")

        team = TeamService.get_team(data.get('id'))
        user = Users.query.get(data.get('user_id'))
        for t in user.teams:
            if t.id == team.id:
                raise ValueError(f"User {user.name} is already in team {team.name}")

        user.teams.append(team)

        db.session.commit()


    @staticmethod
    def get_project_teams(project_id):
        project = Project.query.get(project_id)
        if project is None:
            raise ValueError(f"Project with id {project_id} not found")

        teams = Team.query.filter_by(projectID=project_id).all()
        return teams

    @staticmethod
    def get_project_members(project_id):
        project = Project.query.get(project_id)
        if project is None:
            raise ValueError(f"Project with id {project_id} not found")

        members = {}
        for team in project.teams:
            for user in team.users:
                members[user.id] = user

        return sorted(members.values(), key=lambda user: user.id)

    @staticmethod
    def get_participating_teams(user_id):
        teams = Users.query.get(user_id).teams
        return teams
