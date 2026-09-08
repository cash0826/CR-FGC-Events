from models.events import Event
from .base_service import BaseService
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from config import db

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

  @classmethod
  def update_event(cls, event_id, data):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
      return None, "event_not_found"    
    try:
      if 'start' in data and isinstance(data['start'], str):
        data['start'] = datetime.fromisoformat(data['start'])
      if 'end' in data and isinstance(data['end'], str):
        data['end'] = datetime.fromisoformat(data['end'])
      for key, value in data.items():
        setattr(event, key, value)
      db.session.commit()
      return event, None
    except IntegrityError:
      db.session.rollback()
      return None, "duplicate"
    except Exception:
      db.session.rollback()
      return None, 'invalid_date'