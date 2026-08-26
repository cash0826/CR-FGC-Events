from .base_controller import BaseController
from services.tournaments_service import TournamentService
from schemas.tournament_schema import TournamentSchema

class TournamentsController(BaseController):
    service = TournamentService
    schema = TournamentSchema()