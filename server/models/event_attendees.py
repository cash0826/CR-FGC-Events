from app import db
from sqlalchemy.orm import validates

class EventAttendee(db.Model):
  __tablename__ = 'event_attendees'
  
  id = db.Column(db.Integer, primary_key=True)
  
  # Foreign Keys to store User and Event
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
  
  # Relationship Mapping
  user = db.relationship(
    'User',
    back_populates='event_attendance'
  )
  
  event = db.relationship(
    'Event',
    back_populates='attendees'
  )
  
  @validates('user_id', 'event_id')
  def validate_ids(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
  
  def __repr__(self):
    return (
      f"<EventAttendee id={self.id} "
      f"user_id={self.user_id} "
      f"event_id={self.event_id}>"
    )