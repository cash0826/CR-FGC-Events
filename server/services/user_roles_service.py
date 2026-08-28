from models.user_roles import UserRole
from .base_service import BaseService
from models.roles import Role
from sqlalchemy.exc import IntegrityError

class UserRoleService(BaseService):
  model = UserRole
  
  @staticmethod
  def assign_role(cls, user_id, role_name):
    role = Role.query.filter_by(name=role_name).first()
    if not role:
      return None, "role_not_found"
    
    existing = UserRoles.query.filter_by(user_id=user_id, role_id=role.id).first()
    if existing:
      return None, "duplicate"
    
    data = {
      "user_id": user_id,
      "role_id": role.id
    }
    
    return cls.create(data)
  
  @staticmethod
  def remove_role(cls, user_id, role_name):
    role = Role.query.filter_by(name=role_name).first()
    if not role:
      return None, "role_not_found"
    
    instance = UserRole.query.filter_by(user_id=user_id, role_id=role.id).first()
    if not instance:
      return None, "not_found"
    
    return cls.delete(instance.id)