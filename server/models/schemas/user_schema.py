from marshmallow import Schema, fields, validate

class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  email = fields.Email(required=True, validate=validate.Length(max=255))
  username = fields.Str(required=True, validate=validate.Length(min=1, max=50))
  full_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
  bio = fields.Str(allow_none=True)
  profile_pic_url = fields.Str(validate=validate.Length(max=500))
  contact_number = fields.Str(validate=validate.Length(max=50))
  
  x_user = fields.Str(validate=validate.Length(max=255))
  discord_user = fields.Str(validate=validate.Length(max=255))
  twitch_tv_user = fields.Str(validate=validate.Length(max=255))
  xbox_user = fields.Str(validate=validate.Length(max=255))
  steam_user = fields.Str(validate=validate.Length(max=255))
  epic_games_user = fields.Str(validate=validate.Length(max=255))
  battle_net_user = fields.Str(validate=validate.Length(max=255))
  riot_games_user = fields.Str(validate=validate.Length(max=255))
  created_at = fields.DateTime(dump_only=True)
  updated_at = fields.DateTime(dump_only=True)
  
  roles = fields.Nested('UserRoleSchema', many=True, dump_only=True)
  event_attendance = fields.Nested('EventAttendeeSchema', many=True, dump_only=True)
  tournament_competitions = fields.Nested('TournamentCompetitorSchema', many=True, dump_only=True)
  
  # When serializing, remember that Marshmallow will allow clients to send id, created_at, and updated_at. 
  # Use dump_only=True so that clients cannot send this information
  # Use load_only=True for attributes like passwords
  
  # No need for validate.Length(min=1) on Email because Email() already enforces non empty