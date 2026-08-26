from flask_jwt_extended import get_jwt_identity

class OwnershipMixin:

    owner_field = "user_id"   # subclasses can override this

    def require_owner(self, instance):
        current_user_id = get_jwt_identity()

        # If the model doesn't have the owner field, this is a dev error
        if not hasattr(instance, self.owner_field):
            return {"error": "ownership_field_missing"}, 500

        instance_owner_id = getattr(instance, self.owner_field)

        if instance_owner_id != current_user_id:
            return {"error": "forbidden"}, 403

        return None  # success