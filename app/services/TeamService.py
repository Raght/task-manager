from ..model.Project import Project


class TeamService:
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
