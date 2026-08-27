from marshmallow import Schema, fields, validate

class EventAttendeeSchema(Schema):
  id = fields.Int(dump_only=True)
  
  # POST/PUT
  user_id = fields.Int(required=True)
  event_id = fields.Int(required=True)
  
  # GET
  user = fields.Nested('UserSchema', dump_only=True)