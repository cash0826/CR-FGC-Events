from marshmallow import Schema, fields, validate

class MatchSchema(Schema):
  id = fields.Int(dump_only=True)
  round = fields.Str(allow_none=True, validate=validate.Length(max=50))
  start_time = fields.DateTime(allow_none=True)
  status = fields.Str(
    required=True,
    validate=validate.OneOf(["pending", "in_progress", "completed", "cancelled"])
  )
  
  tournament_id = fields.Int(required=True)
  winner_id = fields.Int(allow_none=True)
  
  # Has many
  players = fields.Nested('PlayerSchema', many=True, dump_only=True)
  
  # Has one
  winner = fields.Nested('PlayerSchema', dump_only=True)
  
# Note for future change. Consider adding Bracket to relate to Match
# For now, they both belong to a single event but are separate tables