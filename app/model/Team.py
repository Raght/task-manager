from ..extensions import db

class Team(db.Model):
    __tablename__ = 'team'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    projectID = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    
    # Relationship to Project is defined in Project model
    # Relationship to Users is defined in Users model via team_user association table
