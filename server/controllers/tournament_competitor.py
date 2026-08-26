from .base_controller import BaseController
from services.tournament_competitors_service import TournamentCompetitorService
from schemas.tournament_competitor_schema import TournamentCompetitorSchema

class TournamentCompetitorsController(BaseController):
    service = TournamentCompetitorService
    schema = TournamentCompetitorSchema()