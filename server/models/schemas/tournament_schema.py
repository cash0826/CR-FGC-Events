from marshmallow import Schema, fields, validate

class TournamentSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
  start_time = fields.DateTime(required=True)
  registration_deadline = fields.DateTime(required=True)
  game = fields.Str(allow_none=True, validate=validate.Length(max=255))
  platform = fields.Str(allow_none=True, validate=validate.Length(max=255))
  line_up_type = fields.Str(required=True)
  
  event_id = fields.Int(required=True)
  
  # Has many Competitors, Matches, Standings, and Brackets
  competitors = fields.Nested(TournamentCompetitorSchema, many=True, dump_only=True)
  matches = fields. Nested("MatchSchema", many=True, dump_only=True)
  standings = fields.Nested('StandingSchema', many=True, dump_only=True)
  bracket = fields.Nested('BracketSchema', dump_only=True)