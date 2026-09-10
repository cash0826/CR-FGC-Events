from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services.users_service import UserService
from services.user_roles_service import UserRoleService
from services.auth_service import AuthService

# -------------------------
# Admin-only Role Management
# -------------------------
class UserRoles(Resource):
  
  # POST /users/<user_id>/roles
  @jwt_required()
  def post(self, user_id):
    AuthService.require_admin()
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
    
    role_name = data.get("role")
    
    instance, error = UserRoleService.assign_role(user_id, role_name)
    
    if error == "role_not_found":
      return {"error": "role_not_found"}, 404
    if error == "duplicate":
      return {"error": "duplicate"}, 409
    if error:
      return {"error": error}, 400
    
    roles = UserService.get_roles_for_user(user_id)
    return {"user_id": user_id, "roles": roles}, 201
  
  # DELETE /users/<user_id>/roles/<role_name>
  @jwt_required()
  def delete(self, user_id, role_name):
    AuthService.require_admin()
    
    success, error = UserRoleService.remove_role(user_id, role_name)
    
    if error == "role_not_found":
      return {"error": "role_not_found"}, 404
    if error == "not_found":
      return {"error": "not_found"}, 404
    if error:
      return {"error": "delete_failed"}, 400
    
    roles = UserService.get_roles_for_user(user_id)
    return {"user_id": user_id, "roles": roles}, 200