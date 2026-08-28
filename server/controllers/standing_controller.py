from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services.events_service import EventService
from services.tournaments_service import TournamentService
from services.standings_service import StandingService
from services.auth_service import AuthService
from models.schemas.standing_schema import StandingSchema

standing_schema = StandingSchema()
standings_schema = StandingSchema(many=True)

# List standings, create standings (host/admin), update points post-match, delete standings

class Standings(Resource):
  
  # GET /events/<event_id>/tournaments/<tournament_id>/standings
  def get(self, event_id, tournament_id):
    event = EventService.get_by_id(event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    standings = StandingService.get_all(filters={"tournament_id": tournament_id})
    return standings_schema.dump(standings), 200
  
  # POST /events/<event_id>/tournaments/<tournament_id>/standings
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
    new_standing, error = StandingService.create(data)
    if error:
      return {"error": error}, 400
    return standing_schema.dump(new_standing), 201
  
class StandingDetails(Resource):
  
  # PATCH /events/<event_id>/tournaments/<tournament_id>/standings/<standing_id>
  @jwt_required()
  def patch(self, event_id, tournament_id, standing_id):
    event = EventService.get_by_id(event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    AuthService.require_owner_or_admin(event.host_id)
    
    standing = StandingService.get_by_id(standing_id)
    if not standing or standing.tournament_id != tournament_id:
      return {"error": "standing_not_found"}, 404
    
    data = request.get_json()
    if not data:
      abort(400, description="Missing JSON data")
      
    updated_standing, error = StandingService.update(standing_id, data)
    if error:
      return {"error": error}, 400
    return standing_schema.dump(updated_standing), 200
  
  # DELETE /events/<event_id>/tournaments/<tournament_id>/standings/<standing_id>
  @jwt_required()
  def delete(self, event_id, tournament_id, standing_id):
    event = EventService.get_by_id(event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    AuthService.require_owner_or_admin(event.host_id)
    
    standing = StandingService.get_by_id(standing_id)
    if not standing or standing.tournament_id != tournament_id:
      return {"error": "standing_not_found"}, 404
    
    success, error = StandingService.delete(standing_id)
    if error:
      return {"error": error}, 400
    return {"message": "deleted"}, 200