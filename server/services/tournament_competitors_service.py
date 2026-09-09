from config import db
from models.tournaments import Tournament
from models.tournament_competitors import TournamentCompetitor
from .base_service import BaseService
from services.user_roles_service import UserRoleService
from sqlalchemy.exc import IntegrityError

class TournamentCompetitorService(BaseService):
  model = TournamentCompetitor

  @staticmethod
  def register_user(user_id, tournament_id):
    tournament = Tournament.query.filter_by(id=tournament_id).first()
    if not tournament:
      return None, "tournament_not_found"

    existing = TournamentCompetitor.query.filter_by(user_id=user_id, tournament_id=tournament_id).first()
    if existing:
      return None, "already_registered"

    try:
      competitor = TournamentCompetitor(user_id=user_id, tournament_id=tournament_id)
      db.session.add(competitor)
      db.session.commit()
      # Try assigning player role (non-fatal)
      try:
        UserRoleService.assign_role(user_id, "player")
      except Exception:
        pass
      return competitor, None
    except IntegrityError:
      db.session.rollback()
      return None, "duplicate"
    except ValueError as error:
      db.session.rollback()
      return None, str(error)
    except Exception:
      db.session.rollback()
      return None, "invalid_data"
