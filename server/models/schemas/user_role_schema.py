from marshmallow import Schema, fields, validate

class UserRoleSchema(Schema):
  id = fields.Int(dump_only=True)
  
  # POST/PUT
  user_id = fields.Int(required=True)
  role_id = fields.Int(required=True)
  
  # Single-object relationships (belongs to)
  role = fields.Nested('RoleSchema', dump_only=True )
  