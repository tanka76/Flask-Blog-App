import os
import enum
from app import db,ma 
from sqlalchemy import Enum
from werkzeug.security import check_password_hash,generate_password_hash
from db.base import BaseModel

class UserRoleEnum(enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    CUSTOMER = "user"


#Create Base models and user created_at and updated_at(abstract models)

class Users(BaseModel):
    __tablename__ = "users_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    full_name = db.Column(db.String(255), nullable=True)

    isauthorized = db.Column(db.Boolean, nullable=False, default=False)
    role = db.Column(
        Enum(
            "super_admin",
            "admin",
            "user",
            name="user_role_enum",
        ),
        nullable=False,
        default="user",
    )

    #model methods
    def set_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)






