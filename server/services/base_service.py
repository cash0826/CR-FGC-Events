from sqlalchemy.exc import IntegrityError
from config import db

# Eliminates repeated CRUD boilerplate code
# Allows model-specific overrides
 
# controllers call: 
# Event.create(request.json)
# Event.get_all()
# Event.update(event_id, request.json)

class BaseService:

    model = None   # Subclasses must set this

    @classmethod
    def create(cls, data):
        instance = cls.model(**data)

        try:
            db.session.add(instance)
            db.session.commit()
            return instance, None
        except IntegrityError:
            db.session.rollback()
            return None, "duplicate"
        except Exception:
            db.session.rollback()
            return None, "invalid_data"

    @classmethod
    def get_by_id(cls, instance_id):
        return cls.model.query.filter_by(id=instance_id).first()

    @classmethod
    def get_all(cls):
        return cls.model.query.all()

    @classmethod
    def update(cls, instance_id, data):
        instance = cls.get_by_id(instance_id)
        if not instance:
            return None, "not_found"

        try:
            for key, value in data.items():
                setattr(instance, key, value)

            db.session.commit()
            return instance, None
        except IntegrityError:
            db.session.rollback()
            return None, "duplicate"
        except Exception:
            db.session.rollback()
            return None, "invalid_data"

    @classmethod
    def delete(cls, instance_id):
        instance = cls.get_by_id(instance_id)
        if not instance:
            return None, "not_found"

        try:
            db.session.delete(instance)
            db.session.commit()
            return True, None
        except Exception:
            db.session.rollback()
            return False, "delete_failed"
