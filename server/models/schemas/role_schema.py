from marshmallow import Schema, fields, validate

class RoleSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(
    required=True, 
    validate=validate.OneOf(["admin", "host", "player", "viewer"])
  )
  description = fields.Str(allow_none=True)
  is_system_role = fields.Bool(dump_only=True)
