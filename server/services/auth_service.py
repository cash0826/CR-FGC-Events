from services.users_service import UserService
from flask_jwt_extended import get_jwt_identity
from flask import abort

class AuthService:
  
  @staticmethod
  def get_current_user_id():
    return get_jwt_identity()
  
  @staticmethod
  def get_roles_for_user(user_id=None):
    """
    Returns a list of role names for the given user.
    If user_id is None, users the JWT identity.
    """
    if user_id = None:
      user_id = get_jwt_identity()
    roles = UserService.get_roles_for_user(user_id)
    return roles or []
  
  @staticmethod
  def require_admin(roles=None):
    """
    Abort if the user is not an admin
    """
    if roles is None:
      roles = AuthService.get_roles_for_user()
    if "admin" is not in roles:
      abort(403, description="Admin role required")
      
  @staticmethod
  def require_host_or_admin(roles=None):
    """
    Abort if the user is not a host or an admin
    """
    if roles is None:
      roles = AuthService.get_roles_for_user()
    if "host" not in roles and "admin" not in roles:
      abort(403, description="Host or Admin role required")   
      
  @staticmethod
  def require_owner_or_admin(target_user_id, roles=None):
    """
    Abort unless the user is the owner or an admin
    """
    current_user_id = get_jwt_identity()
    
    if roles is None:
      roles = AuthService.get_roles_for_user(current_user_id)
    if current_user_id != target_user_id and "admin" not in roles:
      abort(403, description="Forbidden: not owner or admin")
