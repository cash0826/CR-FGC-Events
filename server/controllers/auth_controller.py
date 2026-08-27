from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from services.users_service import UserService
from schemas.user_schema import UserSchema

# global contact schema instance for serialization
user_schema = UserSchema()

# /me GET
class Me(Resource):
  @jwt_required()
  def get(self):
    user_id = get_jwt_identity()
    user = UserService.get_user_by_id(user_id)
    if not user:
      return {"error": "not_found"}, 404
    return user_schema.dump(user), 200
    
# /register POST
class Register(Resource):
  def post(self):
    data = request.get_json()
    user, error = UserService.create_user(data)
    token = create_access_token(identity=user.id)
    return {
      "message": "Registered",
      "token": token,
      "user": user_schema.dump(user)
    }, 201

# /login POST
class Login(Resource):
  def post(self):
    data = request.get_json()
    
    email = data.get("email")
    password = data.get("password")
    user = UserService.get_user_by_email(email)
    if user and user.authenticate(password):
      token = create_access_token(identity=user.id)
      return {
        "message": "Logged_In",
        "token": token,
        "user": user_schema.dump(user)
      }, 200
    return {"error": "invalid_credentials"}, 401
  
  # Logout is controlled by frontend. 
  # Remember to clear JWT token on frontend