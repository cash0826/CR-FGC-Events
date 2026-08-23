from marshmallow import Schema, fields, validate

class PlayerSchema(Schema):
  id = fields.Int(dump_only=True)
  
  competitor_id = fields.Int(required=True, dump_only=True)
  match_id = fields.Int(required=True)
  
  competitor = fields.Nested(TournamentCompetitorSchema, dump_only=True)