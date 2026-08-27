from models.tournaments import Tournament
from .base_service import BaseService

class TournamentService(BaseService):
  model = Tournament
  
  @classmethod
  def get_tournaments_by_event(cls, event_id):
    return cls.model.query.filter_by(event_id=event_id).all()
  
  @classmethod
  def create_tournament(cls, event_id, data):
    data["event_id"] = event_id
    return cls.create(data)