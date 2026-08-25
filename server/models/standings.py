from app import db
from sqlalchemy.orm import validates

class Standing(db.Model):
  __tablename__ = 'standings'
  
  id = db.Column(db.Integer, primary_key=True)
  competitor_id = db.Column(db.Integer, db.ForeignKey('tournament_competitors.id'), nullable=False)
  points = db.Column(db.Integer, nullable=False)
  tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
  
  # Belongs to one
  competitor = db.relationship('TournamentCompetitor', back_populates='standings')
  tournament = db.relationship('Tournament', back_populates='standings')

  @validates('competitor_id', 'tournament_id', 'points')
  def validate_int_fields(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    if key == "points" and value < 0:
      raise ValueError("points cannot be negative")
    return value
      
  def __repr__(self):
    return f"<Standing competitor_id={self.competitor_id} points={self.points}>"