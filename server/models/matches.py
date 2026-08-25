from config import db
from sqlalchemy.orm import validates
from datetime import datetime

class Match(db.Model):
  __tablename__ = "matches"
  
  id = db.Column(db.Integer, primary_key=True)
  round = db.Column(db.String(50), nullable=True)
  start_time = db.Column(db.DateTime, nullable=True)
  status = db.Column(db.String(50), default='pending', nullable=False)
  # status allowed per validation: pending, in_progress, cancelled, completed
  
  # Foreign Keys
  tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
  winner_id = db.Column(db.Integer, db.ForeignKey('tournament_competitors.id'), nullable=True)
  
  # Belongs to
  tournament = db.relationship('Tournament', back_populates='matches')
  
  # Has many
  players = db.relationship(
    'Player',
    back_populates='match',
    foreign_keys='Player.match_id',
    cascade='all, delete-orphan'
  )
  
  # Has one
  winner = db.relationship('TournamentCompetitor', foreign_keys=[winner_id])
  
  # Validation
  @validates('status')
  def validate_status(self, key, value):
    allowed = {"pending", "in_progress", "completed", "cancelled"}
    if value not in allowed:
      raise ValueError(f"Invalid match status: {value}")
    return value

  @validates('winner_id')
  def validate_winner(self, key, value):
    if value is None:
      return value
    competitor_ids = {p.competitor_id for p in self.players}
    if value not in competitor_ids:
      raise ValueError("Winner must be one of the match competitors.")
    return value

  def __repr__(self):
    return f"<Match id={self.id} event_id={self.event_id} status={self.status}>"