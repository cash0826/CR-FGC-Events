from app import db
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
  winner_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
  
  # Belongs to
  tournament = db.relationship('Tournament', back_populates='match')
  
  # Has many
  players = db.relationship(
    'Player',
    back_populates='match',
    cascade='all, delete-orphan'
  )
  
  # Has one
  winner = db.relationship('Player', foreign_keys=[winner_id])
  
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
    player_ids = {p.player_id for p in self.players}
    if value not in player_ids:
      raise ValueError("Winner must be one of the match players.")
    return value

  def __repr__(self):
    return f"<Match id={self.id} event_id={self.event_id} status={self.status}>"