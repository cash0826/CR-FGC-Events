from .base_controller import BaseController
from services.tournaments_service import TournamentService
from schemas.tournament_schema import TournamentSchema
from mixins.role_required_mixin import AdminRequiredMixin

class AdminTournamentsController(BaseController):
  service = TournamentService
  schema = TournamentSchema()
  rbac = AdminRequiredMixin()