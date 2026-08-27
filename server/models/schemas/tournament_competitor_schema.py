from marshmallow import Schema, fields, validate

class TournamentCompetitorSchema(Schema):
  id = fields.Int(dump_only=True)
  user_id = fields.Int(required=True)
  tournament_id = fields.Int(required=True)
  
  # Belongs to one User
  user = fields.Nested('UserSchema', dump_only=True)