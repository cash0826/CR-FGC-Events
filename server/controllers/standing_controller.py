from .base_controller import BaseController
from services.standings_service import StandingService
from schemas.standing_schema import StandingSchema

class Controller(BaseController):
    service = StandingService
    schema = StandingSchema()