from app import db
from sqlalchemy.orm import validates

class TournamentCompetitor(db.Model):
  __tablename__ = 'tournament_competitors'
  
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  tournament_id = db.Column(db.Integer, db. ForeignKey('tournaments.id'), nullable=False)
  
  # Relationships
  user = db.relationship(
    'User',
    back_populates='tournament_competitions'
  )
  
  tournament = db.relationship(
    'Tournament',
    back_populates='competitors'
  )
  
  players = db.relationship(
    'Player',
    back_populates='competitor',
    foreign_keys='Player.competitor_id',
    cascade='all, delete-orphan'
  )
  
  standings = db.relationship(
    'Standing',
    back_populates='competitor',
    cascade='all, delete-orphan'
  )
  
  @validates('user_id', 'tournament_id')
  def validate_tournament_id(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
  
  def __repr__(self):
    return f"<TournamentCompetitor id={self.id} user_id={self.user_id}>"