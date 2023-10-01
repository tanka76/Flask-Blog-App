from flask_jwt_extended import create_access_token,create_refresh_token


def generate_jwt_token(payload,fresh=None):
    data={}
    if fresh:
        data['access_token']=create_access_token(identity=payload,fresh=True)
        data['refresh_token']=create_refresh_token(identity=payload)
        return data
    data['access_token']=create_access_token(identity=payload)
    data['refresh_token']=create_refresh_token(identity=payload)
    return data
