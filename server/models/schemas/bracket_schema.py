from marshmallow import Schema, fields, validate

class BracketSchema(Schema):
  id = fields.Int(dump_only=True)
  url = fields.Str(required=True)
  event_id = fields.Int(required=True)
