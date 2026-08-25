from .base_controller import BaseController
from services.tournament_competitors_service import TournamentCompetitorService
from schemas.tournament_competitor_schema import TournamentCompetitorSchema

class Controller(BaseController):
    service = TournamentCompetitorService
    schema = TournamentCompetitorSchema()