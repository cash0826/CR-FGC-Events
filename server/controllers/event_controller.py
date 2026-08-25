from .base_controller import BaseController
from service.events_service import EventService
from schemas.event_schema import EventSchema

class Controller(BaseController):
    service = EventService
    schema = EventSchema()