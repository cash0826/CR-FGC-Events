from marshmallow import Schema, fields

class EventSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  start = fields.DateTime(required=True)
  end = fields.DateTime(allow_none=True)
  in_person = fields.Bool(allow_none=True)
  location = fields.Str(allow_none=True)
  description = fields.Str(allow_none=True)
  tie_breaking_rule = fields.Str(allow_none=True)
  created_at = fields.DateTime(dump_only=True)
  
  # POST/PUT 
  host_id = fields.Int(required=True)
  
  # Has one Host (read-only)
  host = fields.Nested(UserSchema, dump_only=True)
  # Has many (read-only)
  attendees = fields.Nested(EventAttendeeSchema, many=True, dump_only=True)
  tournaments = fields.Nested('TournamentSchema', many=True, dump_only=True)


  