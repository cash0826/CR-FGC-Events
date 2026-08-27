from sqlalchemy.exc import IntegrityError
from config import db
from models.users import User

# Services control queries, commits, rollbacks and try/except blocks
# Omitting using base_service so I can refer back to a service layer. User also requires pw hashing

class UserService:
  
  @staticmethod
  # Handles hashing, validation, and persistance
  def create_user(data):
    email = data.get('email')
    username = data.get('username')
    if User.query.filter_by(email=email).first():
      return None, "duplicate_email"
    if User.query.filter_by(username=username).first():
      return None, "duplicate_username"
    
    user = User(
      email=email,
      username=username,
      full_name=data.get('full_name'),
      date_of_birth=data.get('date_of_birth'),
    )
    raw_password = data.get('password')
    user.password_hash = password
    
    try:
      db.session.add(user)
      db.session.commit()
      return user, None
    except IntegrityError:
      db.session.rollback()
      return None, "duplicate"
    except Exception:
      db.session.rollback()
      return None, "invalid_data"
    
  @staticmethod
  # Used by controllers for profile pages, authentication, and resource-ownership checks
  def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()
  
  @staticmethod
  # Required for login, registration validation and uniqueness_checks
  def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
  
  @staticmethod
  # Lists all users, helpful for admin dashboards, search and pagination
  def get_all_users():
    return User.query.all()

  @staticmethod
  # Supports profile editing and settings
  def update_user(user_id, data):
    user = User.query.filter_by(id=user_id).first()
    if not user:
      return None, "not_found"
    try:
      if "password" in data:
        user.password_hash(data.get('password'))
        data.pop("password")
      for key, value in data.items():
        setattr(user, key, value)
      db.session.commit()
      return user, None
    except IntegrityError:
      db.session.rollback()
      return None, "duplicate"
    except Exception:
      db.session.rollback()
      return None, "invalid_data"
        
  @staticmethod
  # Soft delete recommended; hard delete only if safe
  def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
      return None, "not_found"
    try:
      db.session.delete(user)
      db.session.commit()
      return True, None
    except Exception:
      db.session.rollback()
      return False, "delete_failed"