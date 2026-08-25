from .base_controller import BaseController
from services.matches_service import MatchService
from schemas.match_schema import MatchSchema

class Controller(BaseController):
    service = MatchService
    schema = MatchSchema()