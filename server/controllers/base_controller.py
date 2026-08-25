from flask import request
from flask.views import MethodView

class BaseController(MethodView):

    service = None      # Subclasses must set this
    schema = None       # Marshmallow schema (optional but recommended)

    def get(self, instance_id=None):
        if instance_id is None:
            instances = self.service.get_all()
            return self.schema.dump(instances, many=True), 200

        instance = self.service.get_by_id(instance_id)
        if not instance:
            return {"error": "not_found"}, 404

        return self.schema.dump(instance), 200

    def post(self):
        data = request.get_json()
        instance, error = self.service.create(data)

        if error == "duplicate":
            return {"error": "duplicate"}, 409
        if error:
            return {"error": "invalid_data"}, 400

        return self.schema.dump(instance), 201

    def patch(self, instance_id):
        data = request.get_json()
        instance, error = self.service.update(instance_id, data)

        if error == "not_found":
            return {"error": "not_found"}, 404
        if error == "duplicate":
            return {"error": "duplicate"}, 409
        if error:
            return {"error": "invalid_data"}, 400

        return self.schema.dump(instance), 200

    def delete(self, instance_id):
        success, error = self.service.delete(instance_id)

        if error == "not_found":
            return {"error": "not_found"}, 404
        if error:
            return {"error": "delete_failed"}, 400

        return {"message": "deleted"}, 200
