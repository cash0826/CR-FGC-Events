from app import db
from sqlalchemy.orm import validates

class Bracket(db.Model):
  __tablename__ = 'brackets'
  
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.Text, nullable=False)
  tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
  
  # Belongs to one
  tournament = db.relationship('Tournament', back_populates='bracket')
  
  @validates('tournament_id')
  def validate_int_fields(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
  
  def __repr__(self):
    return f"<Bracket id={self.id} url={self.url}>"
