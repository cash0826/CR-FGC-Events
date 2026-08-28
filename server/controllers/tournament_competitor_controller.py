from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.schemas.tournament_competitor_schema import TournamentCompetitorSchema
from services.tournament_competitors_service import TournamentCompetitorService
from services.tournaments_service import TournamentService
from services.events_service import EventService
from services.auth_service import AuthService

competitor_schema = TournamentCompetitorSchema()
competitors_schema = TournamentCompetitorSchema(many=True)

class Competitors(Resource):
  
  # GET /events/<event_id>/tournaments/<tournament_id>/competitors
  def get(self, event_id, tournament_id):
    event = EventService.get_by_id(instance_id=event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(instance_id=tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    competitors = TournamentCompetitorService.get_all(filters={"tournament_id": tournament_id})
    return competitors_schema.dump(competitors)
  
  # POST /events/<event_id>/tournaments/<tournament_id>/competitors
  @jwt_required()
  def post(self, event_id, tournament_id):
    event = EventService.get_by_id(instance_id=event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(instance_id=tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    user_id = AuthService.get_current_user_id()
    
    competitor, error = TournamentCompetitorService.register_user(
      user_id=user_id,
      tournament_id=tournament_id
    )
    
    if error == "already_registered":
      return {"error": "already_registered"}, 409
    if error:
      return {"error": "invalid_data"}, 400
    return competitor_schema.dump(competitor)
  
  # DELETE /events/<event_id>/tournaments/<tournament_id>/competitors/<competitor_id>
  @jwt_required()
  def delete(self, event_id, tournament_id, competitor_id):
    event = EventService.get_by_id(instance_id=event_id)
    if not event:
      return {"error": "event_not_found"}, 404
    tournament = TournamentService.get_by_id(instance_id=tournament_id)
    if not tournament:
      return {"error": "tournament_not_found"}, 404
    
    AuthService.require_owner_or_admin(event.host_id)
    
    competitor = TournamentCompetitorService.get_by_id(competitor_id)
    if not competitor or competitor.tournament_id != tournament_id:
      return {"error": "competitor_not_found"}, 404
    
    success, error =  TournamentCompetitorService.delete(competitor_id)

    if error:
      return {"error": "delete_failed"}, 400
    return {"message": "deleted"}, 200