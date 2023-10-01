from marshmallow import Schema, fields


class UserRegisterSchema(Schema):
    userid=fields.Str(dump_only=True)
    username=fields.Str(required=True)
    password=fields.Str(load_only=True,required=True)
    email=fields.Email()
    isauthorized=fields.Boolean()

class UserSchema(Schema):
    id=fields.Str(dump_only=True)
    name=fields.Str(required=True)


