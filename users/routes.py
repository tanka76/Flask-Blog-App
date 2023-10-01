from flask import jsonify,request
from flask.views import MethodView
import json
from .schema import UserSchema
from .models import Users
from app import db
from flask_smorest import Blueprint

bp = Blueprint("users", __name__)

@bp.route("/",methods=['GET'])
@bp.response(200,UserSchema(many=True))
def get_data():

    return [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]


# @bp.route("/")
class UserView(MethodView):
    def get(self):
        # return json.dump({"Msg":"All Users"})
        return {"Msg":"All Users"}
        return jsonify({"Error": "Unauthorized"}), 401
    



