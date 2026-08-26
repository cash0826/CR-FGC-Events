from flask import request
from flask_restful import Resource

# Handles all HTTP semantics
# Matches BaseService return shapes → (result, error)
# Supports Marshmallow schemas
# Supports both list and detail routes
# Keeps controllers small

class BaseController(Resource):

    service = None      # Subclasses must set this
    schema = None       # Marshmallow schema (optional but recommended)
    ownership = None    # mixin instance, optional
    rbac = None         # RBAC

    def get(self, instance_id=None):
        
        if self.rbac:
            auth_error = self.rbac.require_roles()
            if auth_error:
                return auth_error
        
        # Detail route: /resource/<id>
        if instance_id is not None:
            instance = self.service.get_by_id(instance_id)
            if not instance:
                return {"error": "not_found"}, 404
            return self.schema.dump(instance), 200
        
        # List route: /resource?page=1&per_page=10
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        pagination = self.service.model.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        response = {
            "items": self.schema.dump(pagination.items, many=True),
            "total": pagination.total,
            "current_page": pagination.page,
            "pages": pagination.pages,
            "per_page": pagination.per_page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
            "next_page": pagination.next_num if pagination.has_next else None,
            "prev_page": pagination.prev_num if pagination.has_prev else None,
        }
        return response, 200
        
    def post(self):

        if self.rbac:
            auth_error = self.rbac.require_roles()
            if auth_error:
                return auth_error
            
        data = request.get_json()
        instance, error = self.service.create(data)

        if error == "duplicate":
            return {"error": "duplicate"}, 409
        if error:
            return {"error": "invalid_data"}, 400

        return self.schema.dump(instance), 201

    def patch(self, instance_id):

        if self.rbac:
            auth_error = self.rbac.require_roles()
            if auth_error:
                return auth_error
            
        instance = self.service.get_by_id(instance_id)
        if not instance:
            return {"error": "not_found"}, 404
        # OwnershipMixin
        if self.ownership:
            auth_error = self.ownership.require_owner(instance)
            if auth_error:
                return auth_error

        data = request.get_json()
        updated, error = self.service.update(instance_id, data)
        
        if error == "duplicate":
            return {"error": "duplicate"}, 409
        if error:
            return {"error": "invalid_data"}, 400
        return self.schema.dump(updated), 200

    def delete(self, instance_id):

        if self.rbac:
            auth_error = self.rbac.require_roles()
            if auth_error:
                return auth_error
            
        instance = self.service.get_by_id(instance_id)
        if not instance:
            return {"error": "not_found"}, 404
        # OwnershipMixin
        if self.ownership:
            auth_error =self.ownership.require_owner(instance)
            if auth_error:
                return auth_error
        
        success, error = self.service.delete(instance_id)

        if error:
            return {"error": "delete_failed"}, 400
        return {"message": "deleted"}, 200
