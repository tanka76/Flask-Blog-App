import os
from datetime import timedelta
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_smorest import Api
from users.blacklist import blacklisted_tokens

db = SQLAlchemy()
ma = Marshmallow()
api = Api()
jwt=JWTManager()



def create_app():
    """
    Create a Flask application instance and configure it.
    """
    app = Flask(
        __name__,
        template_folder="../templates/build",
        static_folder="../templates/build/static",
    )

    #Load .env file
    load_dotenv()

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

    #swagger config
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Flask Blog API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"]='/api'
    app.config["OPENAPI_SWAGGER_UI_PATH"]='/swagger-ui'
    app.config["OPENAPI_SWAGGER_UI_URL"]='https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/'

    #redoc
    app.config["OPENAPI_REDOC_PATH"]='/redoc-ui'
    app.config["OPENAPI_REDOC_URL"]='https://rebilly.github.io/ReDoc/releases/v1.x.x/redoc.min.js'

    #add authentication in swagger ui
    app.config['API_SPEC_OPTIONS'] = {
    'security': [{"bearerAuth": []}],
    'components': {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
                }
            }
        },
    'scheme': ['http', 'https']
    }
    app.config['OPENAPI_SWAGGER_UI_PROTOCOLS'] = ['http', 'https']
    #jwt config
    app.config['JWT_SECRET_KEY']=os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES']= timedelta(minutes=300)
    jwt.init_app(app)

    #JWT Error handling
    @jwt.expired_token_loader
    def my_expired_token_callback(jwt_header,jwt_payload):
        return (
            jsonify(
                {"message": "The token has expired. Please generate a new token again."}
            ),
            401,
        )
    
    @jwt.invalid_token_loader
    def my_expired_token_callback(error):
        return (
            jsonify(
                {"message": "Invalid token"}
            ),
            401,
        )
    
    @jwt.unauthorized_loader
    def my_expired_token_callback(error):
        return (
            jsonify(
                {"message": "Request doesnot contains access token"}
            ),
            401,
        )
    
    #logout jwt
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in blacklisted_tokens
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"message": "The token has been revoked"}
            ),
            401,
        )
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"message": "The token is not fresh"}
            ),
            401,
        )
    
    api.init_app(app)


    from users import models

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)

    register_blueprints(app=app)

    return app


def register_blueprints(app):
    from users.routes import bp as users_blueprint
    from blogs.routes import bp as blogs_blueprint

    #we are registering using flask smorest.
    api.register_blueprint(users_blueprint)
    api.register_blueprint(blogs_blueprint)
    


def get_database_uri():
    """
    Construct the database URI based on environment variables.
    """
    database_name = os.getenv("DATABASE_NAME")
    database_username = os.getenv("DATABASE_USERNMAE")
    database_password = os.getenv("DATABASE_PASSWORD")
    host_name = os.getenv("HOST_NAME")
    db_port = os.getenv("DB_PORT")

    return f"postgres://{database_username}:{database_password}@{host_name}:{db_port}/{database_name}"