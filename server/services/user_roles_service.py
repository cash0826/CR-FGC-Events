from config import db
from models.user_roles import UserRole
from .base_service import BaseService
from models.roles import Role
from sqlalchemy.exc import IntegrityError

class UserRoleService(BaseService):
    model = UserRole

    @staticmethod
    def assign_role(user_id, role_name):
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            return None, "role_not_found"

        existing = UserRole.query.filter_by(user_id=user_id, role_id=role.id).first()
        if existing:
            return None, "duplicate"

        try:
            ur = UserRole(user_id=user_id, role_id=role.id)
            db.session.add(ur)
            db.session.commit()
            return ur, None
        except IntegrityError:
            db.session.rollback()
            return None, "duplicate"
        except ValueError as error:
            db.session.rollback()
            return None, str(error)
        except Exception:
            db.session.rollback()
            return None, "invalid"

    @staticmethod
    def remove_role(user_id, role_name):
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            return None, "role_not_found"

        instance = UserRole.query.filter_by(user_id=user_id, role_id=role.id).first()
        if not instance:
            return None, "not_found"

        try:
            db.session.delete(instance)
            db.session.commit()
            return True, None
        except Exception:
            db.session.rollback()
            return False, "delete_failed"

# compatibility alias: some modules import UserRolesService
UserRolesService = UserRoleService
