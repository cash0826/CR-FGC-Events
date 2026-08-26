from .base_controller import BaseController
from services.users_service import UserService
from schemas.user_schema import UserSchema
from mixins.role_required_mixin import AdminRequiredMixin

class AdminUsersController(BaseController):
  service = UserService
  schema = UserSchema()
  rbac = AdminRequiredMixin()