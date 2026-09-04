from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services.events_service import EventService
from services.tournaments_service import TournamentService
from services.matches_service import MatchService
from services.auth_service import AuthService
from models.schemas.match_schema import MatchSchema

match_schema = MatchSchema()
matches_schema = MatchSchema(many=True)

class MatchDetails(Resource):
  
  # GET 1 /events/<event_id>/tournaments/<tournament_id>/matches/<match_id>
  def get(self, event_id, tournament_id, match_id):
    event = EventService.get_by_id(event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    match = MatchService.get_by_id(match_id)
    if not match or match.tournament_id != tournament_id:
      return {"error": "match_not_found"}, 404
    return match_schema.dump(match), 200
  
  # PATCH /events/<event_id>/tournaments/<tournament_id>/matches/<match_id>
  @jwt_required()
  def patch(self, event_id, tournament_id, match_id):
    event = EventService.get_by_id(event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    AuthService.require_owner_or_admin(event.host_id)
    
    match = MatchService.get_by_id(match_id)
    if not match or match.tournament_id != tournament_id:
      return {"error": "match_not_found"}, 404
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
    
    updated_match, error = MatchService.update(match_id, data)
    if error: 
      return {"error": error}, 400
    return match_schema.dump(updated_match), 200
  
  # DELETE /events/<event_id>/tournaments/<tournament_id>/matches/<match_id>
  @jwt_required()
  def delete(self, event_id, tournament_id, match_id):
    event = EventService.get_by_id(event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    AuthService.require_owner_or_admin(event.host_id)
    
    match = MatchService.get_by_id(match_id)
    if not match or match.tournament_id != tournament_id:
      return {"error": "match_not_found"}, 404
    
    success, error = MatchService.delete(match_id)
    if error:
      return {"error": error}, 400
    return {"message": "deleted"}, 200 
    
class Matches(Resource):
  
  # GET /events/<event_id>/tournaments/<tournament_id>/matches
  def get(self, event_id, tournament_id):
    event = EventService.get_by_id(event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    matches = MatchService.get_all(filters={"tournament_id": tournament_id})
    return matches_schema.dump(matches), 200

  # POST /events/<event_id>/tournaments/<tournament_id>/matches
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
    
    new_match, error = MatchService.create(data)
    if error:
      return {"error": error}, 400
    return match_schema.dump(new_match), 201