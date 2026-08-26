from .base_controller import BaseController
from services.user_roles_service import UserRoleService
from schemas.user_role_schema import UserRoleSchema

class UserRolesController(BaseController):
    service = UserRoleService
    schema = UserRoleSchema()