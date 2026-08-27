from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from services.users_service import UserService
from schemas.user_schema import UserSchema
from mixins.ownership_mixin import OwnershipMixin

# global schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Utility functions: fetch roles for current user
def get_current_user_roles():
  user_id = get_jwt_identity()
  roles = UserService.get_roles_for_user(user_id)
  return roles    # returns ["admin", "host", ...]

def require_admin(roles):
  if "admin" not in roles:
    abort(403, description="Admin role required")

def require_owner_or_admin(current_user_id, target_user_id, roles):
  if current_user_id != target_user_id and "admin" not in roles:
    abort(403, description="Forbidden: not owner or admin")

# -------------------------
# Admin-only User Management
# -------------------------
class Users(Resource):
  
  # get /users
  @jwt_required()
  def get(self):
    roles = get_current_user_roles()
    require_admin(roles)
    
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    
    users_query = UserService.get_all_users()
    users = users_query.paginate(
      page=page,
      per_page=per_page,
      error_out=False   
    )
    return {
      "users": users_schema.dump(users.items),
      "total": users.total,
      "pages": users.pages,
      "current_page": users.page
    }, 200
  
  # post /users
  @jwt_required()
  def post(self):
    roles = get_roles_for_user()
    require_admin(roles)
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
      
    user, error = UserService.create_user(data)
    
    if error == "duplicate_email":
      return {"error": "duplicate_email"}, 409
    if error == "duplicate_username":
      return {"error": "duplicate_username"}, 409
    if error == "duplicate":
      return {"error": "duplicate"}, 409
    if error:
      return {"error": "invalid_data"}, 400
    return user_schema.dump(user), 201
  
  # patch /users/<id>
  @jwt_required()
  def patch(self, id):
    roles = get_current_user_roles()
    require_admin(roles)
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
      
    user, error = UserService.update_user(user_id=id, data=data)
    
    if error == "not_found":
      return {"error": "not_found"}, 404
    if error == "duplicate":
      return {"error": "duplicate"}, 409
    if error:
      return {"error": "invalid_data"}, 400
    return user_schema.dump(user), 200
  
  # delete /users/<id>
  @jwt_required()
  def delete(self, id):
    roles = get_current_user_roles()
    require_admin(roles)
    
    success, error = UserService.delete_user(user_id=id)
    
    if error == "not_found":
      return {"error": "not_found"}, 404
    if error:
      return {"error": "delete_failed"}, 400
    return {"message": "deleted"}, 200

# -------------------------
# User Profile (Owner)
# -------------------------
class Profile(Resource):
  # get /profile
  @jwt_required()
  def get(self):
    current_user_id = get_jwt_identity()
    user = UserService.get_user_by_id(current_user_id)
    return user_schema.dump(user), 200

  # patch /profile/<id>
  @jwt_required()
  def patch(self, id):
    current_user_id = get_jwt_identity()
    roles = get_current_user_roles()
    require_owner_or_admin(current_user_id, id, roles)
    
    data = request.get_json()
    if not data:
      abort(description="Missing JSON data", 400)
      
    user, error = UserService.update_user(user_id=id, data=data)
    
    if error == "not_found":
      return {"error": "not_found"}, 404
    if error == "duplicate":
      return {"error": "duplicate"}, 409
    if error:
      return {"error": "invalid_data"}, 400
    return user_schema.dump(user), 200