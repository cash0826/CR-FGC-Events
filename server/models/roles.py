from config import db
from sqlalchemy.orm import validates

class Role(db.Model):
  __tablename__ = "roles"
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), default='viewer', nullable=False)
  description = db.Column(db.Text)
  is_system_role = db.Column(db.Boolean, nullable=False, default=False)
  
  # Relationships
  users = db.relationship(
    'UserRole',
    back_populates='role',
    cascade='all, delete-orphan'
  )
  
  @validates('name')
  def validate_name(self, key, value):
    allowed = {'admin', 'host', 'player', 'viewer'}
    if not isinstance(value, str):
      raise ValueError(f"Role must be a string")
    cleaned = value.strip().lower()
    if cleaned not in allowed:
      raise ValueError(f"Invalid role: {value}")
    return cleaned

  @validates('is_system_role')
  def validate_system_role(self, key, value):
    if not isinstance(value, bool):
      raise ValueError("is_system_role must be a boolean")
    return value
      
  def __repr__(self):
    return f"<Role id={self.id} name={self.name}>"