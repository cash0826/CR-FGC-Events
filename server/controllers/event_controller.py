from .base_controller import BaseController
from service.events_service import EventService
from schemas.event_schema import EventSchema
from mixins.ownership_mixin import OwnershipMixin

class EventOwnership(OwnershipMixin):
    owner_field = "host_id"

class EventsController(BaseController):
    service = EventService
    schema = EventSchema()
    ownership = EventOwnership()
    
