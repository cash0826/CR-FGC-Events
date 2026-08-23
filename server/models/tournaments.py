from app import db
from sqlalchemy.orm import validates
from datetime import datetime

class Tournament(db.Model):
  __tablename__ = 'tournaments'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  registration_deadline = db.Column(db.DateTime, nullable=False)
  game = db.Column(db.String(255), nullable=True)
  platform = db.Column(db.String(255), nullable=True)
  line_up_type = db.Column(db.String(255), nullable=False)
  
  # Foreign Key to store Event
  event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
  
  # Belongs to Event
  Event = db.relationship(
    'Event',
    back_populates='tournaments'
  )
  
  # Has (many) tournament_competitors, Matches and Standings
  competitors = db.relationship(
    'TournamentCompetitor',
    back_populates='tournament',
    cascade='all, delete-orphan'
  )
  
  matches = db.relationship(
    'Match',
    back_populates='tournament',
    cascade='all, delete-orphan'
  )
  
  standings = db.relationship(
    'Standing',
    back_populates='tournament',
    cascade='all, delete-orphan'
  )
  
  # Has (one) bracket 
  bracket = db.relationship(
    'Bracket',
    back_populates='tournament',
    cascade='all, delete-orphan'
  )
  
  @validates('event_id')
  def validate_tournament_id(self, key, value):
    if not isinstance(value, int):
      raise ValueError("event_id must be an integer")
    return value

  @validates('name')
  def validate_name(self, key, value):
    if not value or not isinstance(value, str):
      raise ValueError("Tournament name must be a non-empty string")
    return value.strip()
  
  @validates('line_up_type')
  def validate_line_up_type(self, key, value):
    if not value or not isinstance(value, str):
      raise ValueError("line_up_type must be a non-empty string")
    return value.strip()

  def __repr__(self):
    return f"<Tournament id={self.id} name={self.name}>"
  