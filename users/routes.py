
from flask import jsonify
from .schema import UserRegisterSchema,UserLoginSchema
from .models import Users as UserModel
from .helpers import generate_jwt_token
from app import db
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required,get_jwt,create_access_token,get_jwt_identity
from .blacklist import blacklisted_tokens

bp = Blueprint("users", __name__ ,url_prefix='/users',description='Operation on users')

@bp.route('/',methods=['GET'])
def home():
    return jsonify({'msg':"Hello World!!!!"})

@bp.route('/register', methods=['POST'])
@bp.arguments(UserRegisterSchema)
@bp.response(201,UserRegisterSchema)
def user_create(user_data):
    user_data['username']=user_data.get('email') #add username same as email
    user = UserModel(**user_data)
    user.set_password()
    db.session.add(user)
    db.session.commit()
    return user


@bp.route('/login', methods=['POST'])
@bp.arguments(UserLoginSchema)
def user_login(user_data):
    #generate access and refresh token in login routes
    payload=user_data.get('email')
    data=generate_jwt_token(payload=payload)
    return data

@bp.route('/refresh', methods=['GET'])
@jwt_required(fresh=True)
def get_refresh_token(user_data):
    identity=get_jwt_identity()
    new_token=create_access_token(identity=identity,fresh=False)
    jti=get_jwt()['jti']
    blacklisted_tokens.add(jti)
    return jsonify({'access_token':new_token})

@bp.route('/logout', methods=['DELETE'])
@jwt_required()
def user_logout():
    jti = get_jwt()["jti"]
    blacklisted_tokens.add(jti)
    return jsonify(message="Successfully logged out"), 200




    



