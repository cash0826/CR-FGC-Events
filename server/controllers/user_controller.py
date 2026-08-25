from .base_controller import BaseController
from services.users_service import UserService
from schemas.user_schema import UserSchema

class UsersController(BaseController):
    service = UserService
    schema = UserSchema()
