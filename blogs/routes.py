from flask_jwt_extended import jwt_required

import json

from app import db
from flask_smorest import Blueprint

bp = Blueprint("blogs", __name__ ,url_prefix='/blog',description='Operation on blogs')

@bp.route('/create', methods=['POST'])
@jwt_required()
def post():
    return {"Blog":"Create"}
    






    



