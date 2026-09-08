from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.schemas.event_schema import EventSchema
from services.events_service import EventService
from services.auth_service import AuthService

# global schema
event_schema = EventSchema()
events_schema = EventSchema(many=True)

class Events(Resource):
  
  # get /events
  def get(self):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    
    events_query = EventService.get_all()
    events = events_query.paginate(
      page=page,
      per_page=per_page,
      error_out=False
    )
    return {
      "events": events_schema.dump(events.items),
      "total": events.total,
      "pages": events.pages,
      "current_page": events.page
    }, 200
  
  # post /events
  @jwt_required()
  def post(self):
    AuthService.require_host_or_admin()
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
    
    new_event, error = EventService.create(data=data)
    
    if error == "duplicate":
      return {"error": "duplicate"}, 409
    if error:
      return {"error": "invalid_data"}, 400
    return event_schema.dump(new_event), 201

class EventDetails(Resource):
  
  # get /events/<id>
  def get(self, id):
    event = EventService.get_by_id(instance_id=id)
    return event_schema.dump(event), 200
  
  # patch /events/<id>
  @jwt_required()
  def patch(self, id):
    event = EventService.get_by_id(instance_id=id)
    if not event:
      return {"error": "not_found"}, 404
    
    AuthService.require_owner_or_admin(event.host_id)
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
    
    updated_event, error = EventService.update_event(event_id=event.id, data=data)
    
    if error == "duplicate":
      return {"error": "duplicate"}, 409
    if error:
      return {"error": "invalid_data"}, 400
    return event_schema.dump(updated_event), 200

  # delete /events/<id>
  @jwt_required()
  def delete(self, id):
    event = EventService.get_by_id(instance_id=id)
    if not event:
      return {"error": "not_found"}, 404
    
    AuthService.require_owner_or_admin()
    
    success, error = EventService.delete(instance_id=id)

    if error:
      return {"error": "delete_failed"}, 400
    return {"message": "deleted"}, 200