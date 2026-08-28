from models.tournaments import Tournament
from models.tournament_competitors import TournamentCompetitor
from .base_service import BaseService
from services.user_roles_service import UserRolesService

class TournamentCompetitorService(BaseService):
  model = TournamentCompetitor
  
  @staticmethod
  def register_user(cls, user_id, tournament_id):
    tournament = Tournament.query.filter_by(tournament_id=tournament_id)
    if not tournament:
      return None, "tournament_not_found"
    existing = TournamentCompetitor.query.filter_by(user_id=user_id, tournament_id=tournament_id).first()
    if existing:
      return None, "already_registered"
    
    data = {
      "user_id": user_id,
      "tournament_id": tournament_id
    }
    
    competitor = cls.create(data)
    UserRoleService.assign_role(user_id, "player")
    
    return competitor, None