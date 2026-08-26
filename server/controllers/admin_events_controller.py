from .base_controller import BaseController
from services.events_service import EventService
from schemas.event_schema import EventSchema
from mixins.role_required_mixin import AdminRequiredMixin

class AdminEventsController(BaseController):
  service = EventService
  schema = EventSchema()
  rbac = AdminRequiredMixin()