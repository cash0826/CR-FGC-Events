from app import db
from sqlalchemy.orm import validates

class Player(db.Model):
  __tablename__ = "players"
  
  id = db.Column(db.Integer, primary_key=True)
  
  # Foreign Keys
  competitor_id = db.Column(db.Integer, db.ForeignKey('tournament_competitor.id'),nullable=False) 
  match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
  
  # Relationship
  competitor = db.relationship('TournamentCompetitor', back_populates='players')
  match = db.relationship('Match', back_populates='players')
  
  # Validation
  @validates('competitor_id', 'match_id')
  def validate_ids(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
  
def __repr__(self):
    return f"<Player id={self.id} player_id={self.competitor_id} match_id={self.match_id}>"  