from .base_controller import BaseController
from services.users_service import UserService
from schemas.user_schema import UserSchema
from mixins.ownership_mixin import OwnershipMixin

class UsersController(BaseController):
    service = UserService
    schema = UserSchema()
    ownership = OwnershipMixin()