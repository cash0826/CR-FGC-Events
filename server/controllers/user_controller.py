from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from schemas.user_schema import UserSchema
from services.users_service import UserService
from services.auth_service import AuthService

# global schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# -------------------------
# Admin-only User Management
# -------------------------
class Users(Resource):
  
  # get /users
  @jwt_required()
  def get(self):
    AuthService.require_admin()
    
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
    AuthService.require_admin()
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
      
    new_user, error = UserService.create_user(data)
    
    if error == "duplicate_email":
      return {"error": "duplicate_email"}, 409
    if error == "duplicate_username":
      return {"error": "duplicate_username"}, 409
    if error == "duplicate":
      return {"error": "duplicate"}, 409
    if error:
      return {"error": "invalid_data"}, 400
    return user_schema.dump(new_user), 201
  
  # patch /users/<id>
  @jwt_required()
  def patch(self, id):
    AuthService.require_admin()
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
      
    updated_user, error = UserService.update_user(user_id=id, data=data)
    
    if error == "not_found":
      return {"error": "not_found"}, 404
    if error == "duplicate":
      return {"error": "duplicate"}, 409
    if error:
      return {"error": "invalid_data"}, 400
    return user_schema.dump(updated_user), 200
  
  # delete /users/<id>
  @jwt_required()
  def delete(self, id):
    AuthService.require_admin()
    
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
    AuthService.require_owner_or_admin(id)
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
      
    updated_user, error = UserService.update_user(user_id=id, data=data)
    
    if error == "not_found":
      return {"error": "not_found"}, 404
    if error == "duplicate":
      return {"error": "duplicate"}, 409
    if error:
      return {"error": "invalid_data"}, 400
    return user_schema.dump(updated_user), 200