from marshmallow import Schema, fields, validate

class TournamentCompetitorSchema(Schema):
  id = fields.Int(dump_only=True)
  user_id = fields.Int(required=True)
  tournament_id = fields.Int(required=True)
  
  # Belongs to one User
  # Keep the embedded user shallow so serializing a competitor cannot recurse
  # through User.tournament_competitions back to this competitor.
  user = fields.Nested(
    'UserSchema',
    only=('id', 'email', 'username', 'full_name'),
    dump_only=True
  )