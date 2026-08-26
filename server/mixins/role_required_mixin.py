from flask_jwt_extended import get_jwt_identity
from models.users import User

# Returns 401 if no user
# Returns 403 if user lacks required role

class RoleRequiredMixin:
  required_roles = []   #Subclasses override this
  
  def require_roles(self):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()
    
    if not user:
      return {"error": "unauthorized"}, 401
    
    # User.roles is assumed to be a relationship
    user_roles = {role.name for role in user.roles}
    
    # Check if a user has any of the required roles
    if not any(role in user_roles for role in self.required_roles):
      return {"error": "forbidden"}, 403
    
    return None
  
