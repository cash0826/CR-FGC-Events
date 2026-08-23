from config import db, bcrypt
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
import re

class User(db.Model):
  __tablename__= "users"
  
  # Core Identity
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True, nullable=False, index=True)
  username = db.Column(db.String(50), unique=True, nullable=False, index=True)
  full_name = db.Column(db.String(255), nullable=False)
  _password_hash = db.Column(db.String(255), nullable=False)
  
  # Profile Information
  date_of_birth = db.Column(db.Date, nullable=False)
  bio = db.Column(db.Text, nullable=True)
  profile_pic_url = db.Column(db.String(500), nullable=True)
  
  # Contact Info + Gamer IDs
  contact_number = db.Column(db.String(50), nullable=True)
  x_user = db.Column(db.String(255), nullable=True)
  discord_user = db.Column(db.String(255), nullable=True)
  twitch_tv_user = db.Column(db.String(255), nullable=True)
  xbox_user = db.Column(db.String(255), nullable=True)
  steam_user = db.Column(db.String(255), nullable=True)
  epic_games_user = db.Column(db.String(255), nullable=True)
  battle_net_user = db.Column(db.String(255), nullable=True)
  riot_games_user = db.Column(db.String(255), nullable=True)
  
  # Timestamps
  created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                         onupdate=datetime.utcnow, nullable=False)
  
  # --------------
  # Relationships
  # --------------
  
  # User → Roles (global RBAC). Many to Many 
  roles = db.relationship(
    'UserRole',
    back_populates='user',
    cascade='all, delete-orphan'
  )
  
  # User → Event Host. One to Many
  hosted_events = db.relationship(
    'Event',
    back_populates='host',
    cascade='all, delete-orphan'
  )
  
  # User → Event Attendees. Many to Many
  event_attendance = db.relationship(
    'EventAttendee',
    back_populates="user",
    cascade='all, delete-orphan'
  )
  # User → Tournament Competitors. Many to Many
  tournament_competitions = db.relationship(
    'TournamentCompetitor',
    back_populates='user',
    cascade='all, delete-orphan'
  )

  # Email validation
  @validates('email')
  def validate_email(self, key, address):
    if not isinstance (address, str):
      raise ValueError('Email must be a string')
    address = address.lower().strip()
    if not address:
      raise ValueError("Email cannot be empty")
    if '@' not in address:
      raise ValueError('Email must have @ in the address')
    return address
  
  # Username validation
  @validates("username")
  def validate_username(self, key, value):
      if not value or not value.strip():
          raise ValueError("Username cannot be empty.")
      return value
    
  # Full name validation
  @validates("full_name")
  def validate_full_name(self, key, value):
      if not value or not value.strip():
          raise ValueError("Full name cannot be empty.")
      return value

  # Contact number validation
  @validates("contact_number")
  def validate_contact_number(self, key, number):
    if number is None:
        return number
    # Basic phone validation: digits only, optional + at start
    pattern = r"^\+?\d{7,15}$"
    if not re.match(pattern, number):
        raise ValueError("Phone number must be 7–15 digits, optional leading +.")
    return number

  # DOB Validation
  @validates("date_of_birth")
  def validate_dob(self, key, value):
    if value is None:
      raise ValueError("date_of_birth is required.")
    return value

  # Profile_Pic_URL Validation
  @validates("profile_pic_url")
  def validate_profile_pic_url(self, key, value):
    if value is None:
      return value
    if not isinstance(value, str):
      raise ValueError("Profile picture URL must be a string.")
    if len(value) > 500:
      raise ValueError("Profile picture URL cannot exceed 500 characters.")
    return value.strip()
  
  # Password Hash Constraint
  @hybrid_property
  def password_hash(self):
    raise AttributeError('Password hashes may not be viewed')
  
  # Password Hash Setter
  @password_hash.setter
  def password_hash(self, password):
    if not isinstance(password, str) or len(password.strip()) < 8:
      raise ValueError("Password must be a string of at least 8 characters.")
    password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
    self._password_hash = password_hash.decode('utf-8')
  
  # Password Authenticator
  def authenticate(self, password):
    return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
  
  # --------------
  # Methods
  # --------------
  
  def has_role(self, name: str) -> bool:
    """Check if user has a role by role name."""
    return any(ur.role.name == name for ur in self.roles)

  def __repr__(self):
    return f"<User id={self.id} username={self.username or 'N/A'}>"