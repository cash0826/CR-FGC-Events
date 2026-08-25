from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity
from config import db
from models.users import User

# Services control queries, commits, rollbacks, ownership logic nested validation and try/except blocks

class UserService:
  
  @staticmethod
  # Handles hashing, validation, and persistance
  def create_user():
    request_json = request.get_json()
    
    
  @staticmethod
  # Used by controllers for profile pages, authentication, and resource-ownership checks
  def get_user_by_id():
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first()
    return user
  
  @staticmethod
  # Required for login, registration validation and uniqueness_checks
  def get_user_by_email():
    pass
  
  @staticmethod
  # Lists all users, helpful for admin dashboards, search and pagination
  def get_all_users():
    pass

  @staticmethod
  # Supports profile editing and settings
  def update_user():
    pass
  
  @staticmethod
  # Soft delete recommended; hard delete only if safe
  def delete_user():
    pass