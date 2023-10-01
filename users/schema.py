from marshmallow import Schema, fields,validate,ValidationError,validates
from .models import Users as UserModel

class UserRegisterSchema(Schema):
    rid=fields.Str(dump_only=True)
    password=fields.Str(load_only=True,required=True)
    email=fields.Email(required=True)
    full_name=fields.Str(required=False)
    isauthorized=fields.Boolean(dump_only=True)

        
    @validates('email')
    def validate_email(self,value):
        user=UserModel.query.filter_by(email=value).first()
        if user is not None:
            raise ValidationError("User with this email aleady exist")  

    @validates('password')
    def validate_password(self,value):
        if len(value)<6:
            raise ValidationError("Password must be at least 6 characters long.")     


class UserLoginSchema(Schema):
    email=fields.Email(required=True)
    password=fields.Str(required=True)


