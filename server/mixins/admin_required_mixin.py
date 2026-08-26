from .role_required_mixin import RoleRequiredMixin

class AdminRequiredMixin(RoleRequiredMixin):
  required_roles = ["admin"]