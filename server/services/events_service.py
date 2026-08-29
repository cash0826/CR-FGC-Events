from models.events import Event
from .base_service import BaseService
from datetime import datetime

class EventService(BaseService):
  model = Event

  @classmethod
  def create(cls, data):
    # parse ISO datetime strings if present
    try:
      if 'start' in data and isinstance(data['start'], str):
        data['start'] = datetime.fromisoformat(data['start'])
      if 'end' in data and isinstance(data['end'], str):
        data['end'] = datetime.fromisoformat(data['end'])
    except Exception:
      return None, 'invalid_date'

    return super().create(data)
