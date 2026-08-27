from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from schemas.tournament_schema import TournamentSchema
from services.tournaments_service import TournamentService
from services.events_service import EventService
from services.auth_service import AuthService

# global schema
tournament_schema = TournamentSchema()
tournaments_schema = TournamentSchema(many=True)

# -------------------------
# GET all tournaments - public
# Full CRUD - host or admin
# -------------------------
class EventTournaments(Resource):
  
  # get events/<event_id>/tournaments
  def get(self, event_id):
    event_tournaments = TournamentService.get_tournaments_by_event(event_id)
    return tournaments_schema.dump(event_tournaments), 200
  
  # post events/<event_id>/tournaments
  @jwt_required
  def post(self, event_id):
    event = EventService.get_by_id(instance_id=event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    
    AuthService.require_owner_or_admin(event.host_id)
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
      
    new_tournament, error = TournamentService.create_tournament(event_id=event_id, data=data)
    
    if error = "duplicate":
      return {"error": "duplicate"}, 409
    if error:
      return {"error": "invalid_data"}, 400
    return tournament_schema.dump(new_tournament), 201
  
  # patch /events/<event_id>/tournaments/<tournaments_id>
  @jwt_required
  def patch(self, event_id, tournament_id):
    event = EventService.get_by_id(instance_id=event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(instance_id=tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    AuthService.require_owner_or_admin(event.host_id)
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
    
    updated_tournament, error = TournamentService.update(instance_id=tournament_id, data=data)
    
    if error == "duplicate":
      return {"error": "duplicate"}, 409
    if error:
      return {"error": "invalid_data"}, 400
    return tournament_schema(updated_tournament), 200
  
  # delete /events/<event_id>/tournaments/<tournaments_id>
  @jwt_required
  def delete(self, event_id, tournament_id):
    event = EventService.get_by_id(instance_id=event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(instance_id=tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    AuthService.require_owner_or_admin(event.host_id)
    
    success, error = TournamentService.delete(tournament_id)
    
    if error:
      return {"error": "delete_failed"}, 400
    return {"message": "deleted"}, 200

# -------------------------
# GET tournament details - public
# -------------------------
class ViewTournamentDetails(Resource):
  
  # get /events/<event_id>/tournaments/<tournaments_id>
  def get(sef, event_id, tournament_id):
    event = EventService.get_by_id(instance_id=event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(instance_id=tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    return tournament_schema.dump(tournament), 200