from .base_controller import BaseController
from services.roles_service import RoleService
from schemas.role_schema import RoleSchema

class RolesController(BaseController):
    service = RoleService
    schema = RoleSchema()