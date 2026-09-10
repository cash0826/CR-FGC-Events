from models.tournaments import Tournament
from .base_service import BaseService
from datetime import datetime

class TournamentService(BaseService):
  model = Tournament
  
  @classmethod
  def get_tournaments_by_event(cls, event_id):
    return cls.model.query.filter_by(event_id=event_id).all()
  
  @classmethod
  def create(cls, event_id, data):
    # parse datetime strings
    try:
      if 'start_time' in data and isinstance(data['start_time'], str):
        data['start_time'] = datetime.fromisoformat(data['start_time'])
      if 'registration_deadline' in data and isinstance(data['registration_deadline'], str):
        data['registration_deadline'] = datetime.fromisoformat(data['registration_deadline'])
    except Exception:
      return None, 'invalid_date'
    
    return super().create(data)
  
  @classmethod
  def update(cls, instance_id, data):
    # parse datetime strings
    try:
      if 'start_time' in data and isinstance(data['start_time'], str):
        data['start_time'] = datetime.fromisoformat(data['start_time'])
      if 'registration_deadline' in data and isinstance(data['registration_deadline'], str):
        data['registration_deadline'] = datetime.fromisoformat(data['registration_deadline'])
    except Exception:
      return None, 'invalid_date'
    
    return super().update(instance_id, data)