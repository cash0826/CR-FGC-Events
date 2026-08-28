from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services.events_service import EventService
from services.tournaments_service import TournamentService
from services.brackets_service import BracketService
from services.auth_service import AuthService
from models.schema.bracket_schema import BracketSchema

bracket_schema = BracketSchema()

class Bracket(Resource):
  
  # GET /events/<event_id>/tournaments/<tournament_id>/bracket
  def get(self, event_id, tournament_id):
    event = EventService.get_by_id(event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    bracket = BracketService.get_all(filters={"tournament_id": tournament_id})
    return bracket_schema.dump(bracket), 200
  
  # POST /events/<event_id>/tournaments/<tournament_id>/bracket
  @jwt_required()
  def post(self, event_id, tournament_id):
    event = EventService.get_by_id(event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    AuthService.require_owner_or_admin(event.host_id)
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
    
    data["tournament_id"] = tournament_id
    
    new_bracket, error = BracketService.create(data)
    if error:
      return {"error": error}, 400
    return bracket_schema.dump(new_bracket), 201

class BracketDetails(Resource):
  
  # PATCH /events/<event_id>/tournaments/<tournament_id>/bracket/<bracket_id>
  @jwt_required()
  def patch(self, event_id, tournament_id, bracket_id):
    event = EventService.get_by_id(event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    AuthService.require_owner_or_admin(event.host_id)
    
    bracket = BracketService.get_by_id(bracket_id)
    if not bracket or bracket.tournament_id != tournament_id:
      return {"error": "bracket_not_found"}, 404
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
      
    updated_bracket = BracketService.update(bracket_id, data)
    if error:
      return {"error": error}, 400
    return bracket_schema.dump(updated_bracket), 200
  
  # DELETE /events/<event_id>/tournaments/<tournament_id>/bracket/<bracket_id>
  @jwt_required()
  def delete(self, event_id, tournament_id, bracket_id):
    event = EventService.get_by_id(event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    AuthService.require_owner_or_admin(event.host_id)
    
    bracket = BracketService.get_by_id(bracket_id)
    if not bracket or bracket.tournament_id != tournament_id:
      return {"error": "bracket_not_found"}, 404
    
    success, error = BracketService.delete(bracket_id)
    if error:
      return {"error": error}, 400
    return {"message": "deleted"}, 200