from marshmallow import Schema, fields, validate

class StandingSchema(Schema):
  id = fields.Int(dump_only=True)
  
  competitor_id = fields.Int(required=True)
  points = fields.Int(required=True, validate=validate.Range(min=0))
  tournament_id = fields.Int(required=True)
  
  competitor = fields.Nested('TournamentCompetitorSchema', dump_only=True)