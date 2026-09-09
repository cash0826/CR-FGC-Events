from models.matches import Match
from datetime import datetime
from .base_service import BaseService

class MatchService(BaseService):
  model = Match

  @classmethod
  def create(cls, data):
    # parse ISO datetime strings if present
    try:
      if 'start_time' in data and isinstance(data['start_time'], str):
        data['start_time'] = datetime.fromisoformat(data['start_time'])
    except Exception:
      return None, 'invalid_date'

    return super().create(data)

  @classmethod
  def update(cls, instance_id, data):
    # parse ISO datetime strings if present
    try:
      if 'start_time' in data and isinstance(data['start_time'], str):
        data['start_time'] = datetime.fromisoformat(data['start_time'])
    except Exception:
      return None, 'invalid_date'

    return super().update(instance_id, data)