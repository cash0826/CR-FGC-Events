from .base_controller import BaseController
from services.event_attendees_service import EventAttendeeService
from schemas.event_attendee_schema import Schema

class EventAttendeesController(BaseController):
    service = EventAttendeeService
    schema = EventAttendeeSchema()