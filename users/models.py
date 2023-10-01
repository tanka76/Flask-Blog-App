import os
from app import db,ma 
from sqlalchemy import Enum
from db.base import BaseModel

class UserRoleEnum(Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    CUSTOMER = "customer"


#Create Base models and user created_at and updated_at(abstract models)

class Users(BaseModel):
    __tablename__ = "users_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    isauthorized = db.Column(db.Boolean, nullable=False, default=False)
    
    user_role = db.Column(UserRoleEnum,
        nullable=False,
        default="customer",
    )


    #model methods
    



