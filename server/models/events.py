from config import db
from sqlalchemy.orm import validates
from datetime import datetime

class Event(db.Model):
  __tablename__ = 'events'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  start = db.Column(db.DateTime, nullable=False)
  end = db.Column(db.DateTime, nullable=True)
  in_person = db.Column(db.Boolean, nullable=True)
  location = db.Column(db.String, nullable=True)
  description = db.Column(db.Text, nullable=True)
  tie_breaking_rule = db.Column(db.Text, nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  
  # ForeignKey to store Host
  host_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  
  # Relationships
  host = db.relationship(
    'User', 
    back_populates='hosted_events',
    foreign_keys=[host_id]
  )
  
  attendees = db.relationship(
    'EventAttendee',
    back_populates='event',
    cascade='all, delete-orphan'
  )

  tournaments = db.relationship(
    'Tournament',
    back_populates='event',
    cascade='all, delete-orphan'
  )

  # Validation
  @validates('name')
  def validate_name(self, key, value):
    if not value or not isinstance(value, str):
      raise ValueError("Event name must be a non-empty string")
    return value.strip()
  
  @validates('host_id')
  def validates_ids(self, key, value):
    if value is None:
      return value
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
  
  def __repr__(self):
    return f"<Event id={self.id} name={self.name}>"